from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.manufacturing import JobOrder, JobOrderStatus, ApprovalStatus
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/job-orders", tags=["job-orders"])

class JobOrderBase(BaseModel):
    jo_number: str
    type: str # 'manufacturing' or 'service'
    product_id: uuid.UUID = None
    partner_id: uuid.UUID = None
    start_date: datetime
    end_date: datetime
    tax_rate: float = 0

class JobOrderCreate(JobOrderBase):
    pass

class JobOrderOut(JobOrderBase):
    id: uuid.UUID
    status: JobOrderStatus
    approval_status: ApprovalStatus
    total_cost: float

    class Config:
        from_attributes = True

@router.get("/", response_model=List[JobOrderOut])
async def list_job_orders(db: Session = Depends(get_db)):
    return db.query(JobOrder).all()

@router.post("/", response_model=JobOrderOut)
async def create_job_order(jo_in: JobOrderCreate, db: Session = Depends(get_db)):
    # In reality, get workspace_id from token
    mock_workspace_id = db.query(JobOrder).first().workspace_id if db.query(JobOrder).first() else uuid.uuid4()
    
    db_jo = JobOrder(
        **jo_in.dict(),
        workspace_id=mock_workspace_id,
        status=JobOrderStatus.DRAFT,
        approval_status=ApprovalStatus.DRAFT
    )
    db.add(db_jo)
    db.commit()
    db.refresh(db_jo)
    return db_jo
