from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.procurement import PurchaseOrder, POLine, GoodsReceipt, POStatus
from app.models.ledger import StockLedger, ReferenceType
from app.services.sequence_service import SequenceService
from app.services.journal_service import JournalEngine
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/procurement", tags=["procurement"])

class POItem(BaseModel):
    product_id: uuid.UUID
    qty: float
    unit_price: float
    uom: str

class POCreate(BaseModel):
    partner_id: uuid.UUID
    items: List[POItem]

@router.post("/po")
async def create_po(po_in: POCreate, db: Session = Depends(get_db)):
    # Mock workspace_id
    workspace_id = db.query(PurchaseOrder).first().workspace_id if db.query(PurchaseOrder).first() else uuid.uuid4()
    
    po_number = SequenceService.get_next_number(db, workspace_id, "PO", "PO")
    
    db_po = PurchaseOrder(
        workspace_id=workspace_id,
        po_number=po_number,
        partner_id=po_in.partner_id,
        status=POStatus.DRAFT
    )
    db.add(db_po)
    db.flush()

    total = 0
    for item in po_in.items:
        line = POLine(po_id=db_po.id, **item.dict())
        db.add(line)
        total += item.qty * item.unit_price
    
    db_po.total_amount = total
    db.commit()
    db.refresh(db_po)
    return db_po

@router.post("/grn/{po_id}")
async def receive_goods(po_id: uuid.UUID, warehouse_id: uuid.UUID, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po: raise HTTPException(404, "PO not found")
    
    grn_number = SequenceService.get_next_number(db, po.workspace_id, "GRN", "GRN")
    
    grn = GoodsReceipt(
        workspace_id=po.workspace_id,
        grn_number=grn_number,
        po_id=po_id,
        warehouse_id=warehouse_id,
        received_by=uuid.uuid4() # Mock user
    )
    db.add(grn)
    
    # Update Stock & Trigger Journal
    journal_entries = []
    for line in db.query(POLine).filter(POLine.po_id == po_id).all():
        # Stock Ledger (IN)
        movement = StockLedger(
            product_id=line.product_id,
            warehouse_id=warehouse_id,
            qty=line.qty,
            uom_used=line.uom,
            unit_cost=line.unit_price,
            reference_type=ReferenceType.PO,
            reference_id=grn.id
        )
        db.add(movement)
        
        # Prepare Journal (Debit Inventory, Credit Accrual)
        journal_entries.append({'coa_code': '1103', 'debit': float(line.qty * line.unit_price), 'credit': 0}) # Inventory
        journal_entries.append({'coa_code': '2101', 'debit': 0, 'credit': float(line.qty * line.unit_price)}) # Accrued Liability

    po.status = POStatus.RECEIVED
    db.commit()
    
    # Auto-Journal
    JournalEngine.create_journal_entry(
        db, po.workspace_id, grn_number, 
        f"Inventory Receipt from {po_number}", "GRN", grn.id, journal_entries
    )
    
    return {"message": "Goods received and journaled", "grn": grn_number}
