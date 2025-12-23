from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.notifications import Notification
from app.models.workflow import ApprovalRequest
from app.services.notification_service import NotificationService
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationOut(BaseModel):
    id: uuid.UUID
    type: str
    priority: str
    title: str
    message: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True

class ApprovalOut(BaseModel):
    id: uuid.UUID
    document_type: str
    status: str
    requested_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[NotificationOut])
async def get_notifications(db: Session = Depends(get_db)):
    """Get all notifications for current user"""
    # In production, filter by current user from token
    notifications = db.query(Notification).order_by(Notification.created_at.desc()).limit(50).all()
    return [NotificationOut(
        id=n.id,
        type=n.type,
        priority=n.priority,
        title=n.title,
        message=n.message,
        is_read=n.is_read,
        created_at=str(n.created_at)
    ) for n in notifications]

@router.get("/unread-count")
async def get_unread_count(db: Session = Depends(get_db)):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(Notification.is_read == False).count()
    return {"unread_count": count}

@router.post("/{notification_id}/mark-read")
async def mark_notification_read(notification_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    NotificationService.mark_as_read(db, notification_id)
    return {"message": "Notification marked as read"}

@router.get("/approvals", response_model=List[ApprovalOut])
async def get_approval_requests(db: Session = Depends(get_db)):
    """Get pending approval requests for current user"""
    approvals = db.query(ApprovalRequest).filter(ApprovalRequest.status == "pending").all()
    return [ApprovalOut(
        id=a.id,
        document_type=a.document_type,
        status=a.status,
        requested_at=str(a.requested_at)
    ) for a in approvals]

@router.post("/approvals/{approval_id}/approve")
async def approve_request(approval_id: uuid.UUID, comments: str = None, db: Session = Depends(get_db)):
    """Approve a request"""
    approver_id = uuid.uuid4()  # Mock - get from token
    approval = NotificationService.approve_request(db, approval_id, approver_id, comments)
    return {"message": "Request approved", "approval_id": str(approval.id)}

@router.post("/approvals/{approval_id}/reject")
async def reject_request(approval_id: uuid.UUID, comments: str, db: Session = Depends(get_db)):
    """Reject a request"""
    approver_id = uuid.uuid4()  # Mock - get from token
    approval = NotificationService.reject_request(db, approval_id, approver_id, comments)
    return {"message": "Request rejected", "approval_id": str(approval.id)}
