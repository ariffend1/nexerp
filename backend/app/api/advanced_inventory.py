from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.advanced_inventory_service import AdvancedInventoryService
from pydantic import BaseModel
from datetime import date
from typing import Optional
import uuid

router = APIRouter(prefix="/inventory-advanced", tags=["inventory-advanced"])

# Serial Number Endpoints
class SerialNumberCreate(BaseModel):
    product_id: str
    serial_number: str
    warehouse_id: Optional[str] = None

@router.post("/serial-numbers")
async def create_serial_number(
    data: SerialNumberCreate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Register new serial number"""
    sn = AdvancedInventoryService.create_serial_number(
        db,
        user.workspace_id,
        uuid.UUID(data.product_id),
        data.serial_number,
        uuid.UUID(data.warehouse_id) if data.warehouse_id else None
    )
    return {
        "id": str(sn.id),
        "serial_number": sn.serial_number,
        "status": sn.status
    }

@router.get("/serial-numbers/{product_id}")
async def get_available_serials(
    product_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get available serial numbers for product"""
    serials = AdvancedInventoryService.get_available_serials(
        db, user.workspace_id, uuid.UUID(product_id)
    )
    return {
        "product_id": product_id,
        "available_count": len(serials),
        "serial_numbers": [
            {"id": str(sn.id), "serial_number": sn.serial_number, "status": sn.status}
            for sn in serials
        ]
    }

# Batch/Lot Endpoints
class BatchCreate(BaseModel):
    product_id: str
    batch_number: str
    quantity: int
    warehouse_id: str
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None

@router.post("/batches")
async def create_batch(
    data: BatchCreate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Create batch/lot"""
    batch = AdvancedInventoryService.create_batch(
        db,
        user.workspace_id,
        uuid.UUID(data.product_id),
        data.batch_number,
        data.quantity,
        uuid.UUID(data.warehouse_id),
        date.fromisoformat(data.manufacturing_date) if data.manufacturing_date else None,
        date.fromisoformat(data.expiry_date) if data.expiry_date else None
    )
    return {
        "id": str(batch.id),
        "batch_number": batch.batch_number,
        "quantity_available": batch.quantity_available
    }

@router.get("/batches/expiring")
async def get_expiring_batches(
    days: int = 30,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get batches expiring soon"""
    batches = AdvancedInventoryService.get_expiring_batches(db, user.workspace_id, days)
    return {
        "days_ahead": days,
        "count": len(batches),
        "expiring_batches": [
            {
                "batch_number": b.batch_number,
                "product_id": str(b.product_id),
                "expiry_date": str(b.expiry_date),
                "quantity": b.quantity_available,
                "days_remaining": (b.expiry_date - date.today()).days if b.expiry_date else None
            }
            for b in batches
        ]
    }

# Barcode Endpoints
class BarcodeRegister(BaseModel):
    product_id: str
    barcode: str
    barcode_type: str = "ean13"

@router.post("/barcodes")
async def register_barcode(
    data: BarcodeRegister,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Register barcode for product"""
    mapping = AdvancedInventoryService.register_barcode(
        db, user.workspace_id, uuid.UUID(data.product_id), data.barcode, data.barcode_type
    )
    return {
        "id": str(mapping.id),
        "barcode": mapping.barcode,
        "product_id": str(mapping.product_id)
    }

@router.get("/barcodes/{barcode}")
async def lookup_barcode(
    barcode: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Lookup product by barcode"""
    product = AdvancedInventoryService.lookup_by_barcode(db, user.workspace_id, barcode)
    if not product:
        return {"error": "Product not found"}
    
    return {
        "barcode": barcode,
        "product": {
            "id": str(product.id),
            "code": product.code,
            "name": product.name,
            "type": product.type
        }
    }

# Reorder Rules
class ReorderRuleCreate(BaseModel):
    product_id: str
    warehouse_id: str
    min_quantity: int
    max_quantity: int
    reorder_quantity: int

@router.post("/reorder-rules")
async def create_reorder_rule(
    data: ReorderRuleCreate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Create automatic reorder rule"""
    rule = AdvancedInventoryService.create_reorder_rule(
        db,
        user.workspace_id,
        uuid.UUID(data.product_id),
        uuid.UUID(data.warehouse_id),
        data.min_quantity,
        data.max_quantity,
        data.reorder_quantity
    )
    return {
        "id": str(rule.id),
        "product_id": str(rule.product_id),
        "min_quantity": rule.min_quantity,
        "reorder_quantity": rule.reorder_quantity
    }

@router.get("/reorder-suggestions")
async def get_reorder_suggestions(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get products that need reordering"""
    suggestions = AdvancedInventoryService.check_reorder_points(db, user.workspace_id)
    return {
        "count": len(suggestions),
        "suggestions": suggestions
    }
