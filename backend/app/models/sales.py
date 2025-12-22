import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class SOStatus(str, enum.Enum):
    DRAfT = "draft"
    APPROVED = "approved"
    SHIPPED = "shipped"
    INVOICED = "invoiced"
    CANCELLED = "cancelled"

class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    so_number = Column(String, unique=True, index=True)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id")) # Customer
    status = Column(SqlEnum(SOStatus), default=SOStatus.DRAfT)
    date = Column(DateTime, server_default=func.now())
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(18, 2), default=0)
    total_amount = Column(Numeric(18, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SOLine(Base):
    __tablename__ = "so_lines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    so_id = Column(UUID(as_uuid=True), ForeignKey("sales_orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    qty = Column(Numeric(18, 4))
    unit_price = Column(Numeric(18, 2))
    uom = Column(String)

class DeliveryOrder(Base):
    __tablename__ = "delivery_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    do_number = Column(String, unique=True, index=True)
    so_id = Column(UUID(as_uuid=True), ForeignKey("sales_orders.id"))
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    delivery_date = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
