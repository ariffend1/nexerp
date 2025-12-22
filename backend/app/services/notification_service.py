from sqlalchemy.orm import Session
from app.models.notifications import Notification, NotificationType, NotificationPriority, ApprovalRequest
from datetime import datetime
import uuid

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        workspace_id: uuid.UUID,
        user_id: uuid.UUID,
        type: NotificationType,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        link: str = None
    ):
        """Create a new notification"""
        notification = Notification(
            workspace_id=workspace_id,
            user_id=user_id,
            type=type,
            priority=priority,
            title=title,
            message=message,
            link=link
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    @staticmethod
    def create_approval_request(
        db: Session,
        workspace_id: uuid.UUID,
        document_type: str,
        document_id: uuid.UUID,
        requested_by: uuid.UUID,
        approver_id: uuid.UUID
    ):
        """Create approval request and notify approver"""
        approval = ApprovalRequest(
            workspace_id=workspace_id,
            document_type=document_type,
            document_id=document_id,
            requested_by=requested_by,
            approver_id=approver_id
        )
        db.add(approval)
        db.flush()
        
        # Create notification for approver
        NotificationService.create_notification(
            db,
            workspace_id,
            approver_id,
            NotificationType.APPROVAL_REQUEST,
            f"Approval Required: {document_type}",
            f"A new {document_type} approval is waiting for your review.",
            NotificationPriority.HIGH,
            f"/approvals/{approval.id}"
        )
        
        db.commit()
        return approval
    
    @staticmethod
    def approve_request(db: Session, approval_id: uuid.UUID, approver_id: uuid.UUID, comments: str = None):
        """Approve a request"""
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            raise ValueError("Approval request not found")
        
        approval.status = "approved"
        approval.comments = comments
        approval.responded_at = datetime.utcnow()
        
        # Notify requester
        NotificationService.create_notification(
            db,
            approval.workspace_id,
            approval.requested_by,
            NotificationType.APPROVAL_APPROVED,
            f"{approval.document_type} Approved",
            f"Your {approval.document_type} has been approved.",
            NotificationPriority.MEDIUM,
            f"/{approval.document_type.lower()}/{approval.document_id}"
        )
        
        db.commit()
        return approval
    
    @staticmethod
    def reject_request(db: Session, approval_id: uuid.UUID, approver_id: uuid.UUID, comments: str):
        """Reject a request"""
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            raise ValueError("Approval request not found")
        
        approval.status = "rejected"
        approval.comments = comments
        approval.responded_at = datetime.utcnow()
        
        # Notify requester
        NotificationService.create_notification(
            db,
            approval.workspace_id,
            approval.requested_by,
            NotificationType.APPROVAL_REJECTED,
            f"{approval.document_type} Rejected",
            f"Your {approval.document_type} has been rejected. Reason: {comments}",
            NotificationPriority.HIGH,
            f"/{approval.document_type.lower()}/{approval.document_id}"
        )
        
        db.commit()
        return approval
    
    @staticmethod
    def mark_as_read(db: Session, notification_id: uuid.UUID):
        """Mark notification as read"""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            db.commit()
        return notification
