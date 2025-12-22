import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class JournalStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    POSTED = "posted"
    CANCELLED = "cancelled"

class Journal(Base):
    __tablename__ = "journals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    date = Column(Date)
    ref_no = Column(String, unique=True, index=True)
    description = Column(String)
    source_type = Column(String) # 'PO', 'SO', 'SPK', 'MANUAL', etc.
    source_id = Column(UUID(as_uuid=True), nullable=True)
    approval_status = Column(SqlEnum(JournalStatus), default=JournalStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JournalItem(Base):
    __tablename__ = "journal_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journals.id"))
    coa_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"))
    debit = Column(Numeric(18, 2), default=0)
    credit = Column(Numeric(18, 2), default=0)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True)
    description = Column(String, nullable=True)
