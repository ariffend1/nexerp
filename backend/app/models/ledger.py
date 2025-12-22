import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class ReferenceType(str, enum.Enum):
    PO = "PO"
    SPK = "SPK"
    SO = "SO"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"

class StockLedger(Base):
    __tablename__ = "stock_ledger"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    qty = Column(Numeric(18, 4)) # In base UOM
    uom_used = Column(String)
    unit_cost = Column(Numeric(18, 4))
    reference_type = Column(SqlEnum(ReferenceType))
    reference_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
