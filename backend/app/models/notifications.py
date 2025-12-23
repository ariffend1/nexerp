import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum as SqlEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class NotificationType(str, enum.Enum):
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    LOW_STOCK = "low_stock"
    PAYMENT_DUE = "payment_due"
    TASK_ASSIGNED = "task_assigned"
    SYSTEM_ALERT = "system_alert"

class NotificationPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(SqlEnum(NotificationType))
    priority = Column(SqlEnum(NotificationPriority), default=NotificationPriority.MEDIUM)
    title = Column(String)
    message = Column(Text)
    link = Column(String, nullable=True)  # URL to related item
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
