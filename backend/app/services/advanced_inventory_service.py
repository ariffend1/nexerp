from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, date, timedelta
from ..models.advanced_inventory import SerialNumber, BatchLot, BarcodeMapping, StockReorderRule
from ..models.inventory import Product
from ..models.ledger import StockLedger
import uuid
from typing import Optional, List

class AdvancedInventoryService:
    
    @staticmethod
    def create_serial_number(
        db: Session,
        workspace_id: uuid.UUID,
        product_id: uuid.UUID,
        serial_number: str,
        warehouse_id: Optional[uuid.UUID] = None
    ) -> SerialNumber:
        """Create and track individual serial number"""
        sn = SerialNumber(
            workspace_id=workspace_id,
            product_id=product_id,
            serial_number=serial_number,
            warehouse_id=warehouse_id,
            received_date=date.today(),
            status="available"
        )
        db.add(sn)
        db.commit()
        db.refresh(sn)
        return sn
    
    @staticmethod
    def get_available_serials(
        db: Session,
        workspace_id: uuid.UUID,
        product_id: uuid.UUID
    ) -> List[SerialNumber]:
        """Get all available serial numbers for a product"""
        return db.query(SerialNumber).filter(
            and_(
                SerialNumber.workspace_id == workspace_id,
                SerialNumber.product_id == product_id,
                SerialNumber.status == "available"
            )
        ).all()
    
    @staticmethod
    def create_batch(
        db: Session,
        workspace_id: uuid.UUID,
        product_id: uuid.UUID,
        batch_number: str,
        quantity: int,
        warehouse_id: uuid.UUID,
        manufacturing_date: Optional[date] = None,
        expiry_date: Optional[date] = None
    ) -> BatchLot:
        """Create batch/lot with expiry tracking"""
        batch = BatchLot(
            workspace_id=workspace_id,
            product_id=product_id,
            batch_number=batch_number,
            quantity_total=quantity,
            quantity_available=quantity,
            manufacturing_date=manufacturing_date or date.today(),
            expiry_date=expiry_date,
            warehouse_id=warehouse_id
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch
    
    @staticmethod
    def get_expiring_batches(
        db: Session,
        workspace_id: uuid.UUID,
        days_ahead: int = 30
    ) -> List[BatchLot]:
        """Get batches expiring within specified days"""
        threshold = date.today() + timedelta(days=days_ahead)
        
        return db.query(BatchLot).filter(
            and_(
                BatchLot.workspace_id == workspace_id,
                BatchLot.expiry_date <= threshold,
                BatchLot.expiry_date >= date.today(),
                BatchLot.quantity_available > 0
            )
        ).order_by(BatchLot.expiry_date).all()
    
    @staticmethod
    def register_barcode(
        db: Session,
        workspace_id: uuid.UUID,
        product_id: uuid.UUID,
        barcode: str,
        barcode_type: str = "ean13"
    ) -> BarcodeMapping:
        """Register barcode for product"""
        mapping = BarcodeMapping(
            workspace_id=workspace_id,
            product_id=product_id,
            barcode=barcode,
            barcode_type=barcode_type
        )
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping
    
    @staticmethod
    def lookup_by_barcode(
        db: Session,
        workspace_id: uuid.UUID,
        barcode: str
    ) -> Optional[Product]:
        """Find product by barcode"""
        mapping = db.query(BarcodeMapping).filter(
            and_(
                BarcodeMapping.workspace_id == workspace_id,
                BarcodeMapping.barcode == barcode
            )
        ).first()
        
        if mapping:
            return db.query(Product).filter(Product.id == mapping.product_id).first()
        return None
    
    @staticmethod
    def create_reorder_rule(
        db: Session,
        workspace_id: uuid.UUID,
        product_id: uuid.UUID,
        warehouse_id: uuid.UUID,
        min_quantity: int,
        max_quantity: int,
        reorder_quantity: int
    ) -> StockReorderRule:
        """Create automatic reorder rule"""
        rule = StockReorderRule(
            workspace_id=workspace_id,
            product_id=product_id,
            warehouse_id=warehouse_id,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            reorder_quantity=reorder_quantity
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule
    
    @staticmethod
    def check_reorder_points(db: Session, workspace_id: uuid.UUID) -> List[dict]:
        """Check which products need reordering"""
        reorder_suggestions = []
        
        rules = db.query(StockReorderRule).filter(
            and_(
                StockReorderRule.workspace_id == workspace_id,
                StockReorderRule.is_active == True
            )
        ).all()
        
        for rule in rules:
            # Calculate current stock
            current_stock = db.query(func.sum(StockLedger.quantity)).filter(
                and_(
                    StockLedger.workspace_id == workspace_id,
                    StockLedger.product_id == rule.product_id,
                    StockLedger.warehouse_id == rule.warehouse_id
                )
            ).scalar() or 0
            
            if current_stock < rule.min_quantity:
                product = db.query(Product).filter(Product.id == rule.product_id).first()
                reorder_suggestions.append({
                    "product_id": str(rule.product_id),
                    "product_code": product.code if product else "N/A",
                    "product_name": product.name if product else "N/A",
                    "current_stock": int(current_stock),
                    "min_quantity": rule.min_quantity,
                    "suggested_reorder": rule.reorder_quantity,
                    "urgency": "high" if current_stock < (rule.min_quantity * 0.5) else "medium"
                })
        
        return reorder_suggestions
