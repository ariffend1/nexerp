import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class JobOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ApprovalStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class BillOfMaterials(Base):
    __tablename__ = "bill_of_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BOMItem(Base):
    __tablename__ = "bom_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bom_id = Column(UUID(as_uuid=True), ForeignKey("bill_of_materials.id"))
    component_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    qty = Column(Numeric(18, 4))
    waste_percent = Column(Numeric(5, 2), default=0)

class JobOrder(Base):
    __tablename__ = "job_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    jo_number = Column(String, unique=True, index=True)
    type = Column(String) # 'manufacturing' or 'service'
    status = Column(SqlEnum(JobOrderStatus), default=JobOrderStatus.DRAFT)
    approval_status = Column(SqlEnum(ApprovalStatus), default=ApprovalStatus.DRAFT)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True) # If manufacturing
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True) # If service/project
    
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(18, 2), default=0)
    total_cost = Column(Numeric(18, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
