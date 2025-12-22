from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.sales import SalesOrder, SOLine, DeliveryOrder, SOStatus
from ..models.ledger import StockLedger, ReferenceType
from ..services.sequence_service import SequenceService
from ..services.journal_service import JournalEngine
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/sales", tags=["sales"])

class SOItem(BaseModel):
    product_id: uuid.UUID
    qty: float
    unit_price: float
    uom: str

class SOCreate(BaseModel):
    partner_id: uuid.UUID
    items: List[SOItem]

@router.post("/so")
async def create_so(so_in: SOCreate, db: Session = Depends(get_db)):
    workspace_id = db.query(SalesOrder).first().workspace_id if db.query(SalesOrder).first() else uuid.uuid4()
    so_number = SequenceService.get_next_number(db, workspace_id, "SO", "SO")
    
    db_so = SalesOrder(workspace_id=workspace_id, so_number=so_number, partner_id=so_in.partner_id)
    db.add(db_so)
    db.flush()

    total = 0
    for item in so_in.items:
        line = SOLine(so_id=db_so.id, **item.dict())
        db.add(line)
        total += item.qty * item.unit_price
    
    db_so.total_amount = total
    db.commit()
    return db_so

@router.post("/do/{so_id}")
async def ship_goods(so_id: uuid.UUID, warehouse_id: uuid.UUID, db: Session = Depends(get_db)):
    so = db.query(SalesOrder).filter(SalesOrder.id == so_id).first()
    if not so: raise HTTPException(404, "SO not found")
    
    do_number = SequenceService.get_next_number(db, so.workspace_id, "DO", "DO")
    do = DeliveryOrder(workspace_id=so.workspace_id, do_number=do_number, so_id=so_id, warehouse_id=warehouse_id)
    db.add(do)
    
    journal_entries = []
    for line in db.query(SOLine).filter(SOLine.so_id == so_id).all():
        # Stock Ledger (OUT)
        movement = StockLedger(
            product_id=line.product_id,
            warehouse_id=warehouse_id,
            qty=-line.qty, # Negative for OUT
            uom_used=line.uom,
            unit_cost=line.unit_price, # In production, use valuation method FIFO/Avg
            reference_type=ReferenceType.SO,
            reference_id=do.id
        )
        db.add(movement)
        
        # Journal (Debit AR, Credit Sales / Debit COGS, Credit Inventory)
        amount = float(line.qty * line.unit_price)
        journal_entries.append({'coa_code': '1102', 'debit': amount, 'credit': 0}) # AR
        journal_entries.append({'coa_code': '4101', 'debit': 0, 'credit': amount}) # Sales Revenue

    so.status = SOStatus.SHIPPED
    db.commit()
    
    JournalEngine.create_journal_entry(
        db, so.workspace_id, do_number,
        f"Shipment for {so.so_number}", "DO", do.id, journal_entries
    )
    
    return {"message": "Goods shipped and sales journaled", "do": do_number}
