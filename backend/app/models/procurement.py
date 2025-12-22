import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class POStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    po_number = Column(String, unique=True, index=True)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id")) # Supplier
    status = Column(SqlEnum(POStatus), default=POStatus.DRAFT)
    date = Column(DateTime, server_default=func.now())
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(18, 2), default=0)
    total_amount = Column(Numeric(18, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class POLine(Base):
    __tablename__ = "po_lines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    po_id = Column(UUID(as_uuid=True), ForeignKey("purchase_orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    qty = Column(Numeric(18, 4))
    unit_price = Column(Numeric(18, 2))
    uom = Column(String)

class GoodsReceipt(Base):
    __tablename__ = "goods_receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    grn_number = Column(String, unique=True, index=True)
    po_id = Column(UUID(as_uuid=True), ForeignKey("purchase_orders.id"))
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    received_date = Column(DateTime, server_default=func.now())
    received_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
