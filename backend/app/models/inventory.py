import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ProductType(str, enum.Enum):
    RAW = "raw"
    SEMI_FINISHED = "semi_finished"
    FINISHED = "finished"
    SERVICE = "service"

class ValuationMethod(str, enum.Enum):
    FIFO = "fifo"
    AVERAGE = "average"

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String)
    uom = Column(String) # Base UOM
    type = Column(SqlEnum(ProductType))
    valuation_method = Column(SqlEnum(ValuationMethod), default=ValuationMethod.AVERAGE)
    base_price = Column(Numeric(18, 2), default=0)
    account_id = Column(UUID(as_uuid=True), nullable=True) # Link to COA
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UOMConversion(Base):
    __tablename__ = "uom_conversions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    from_uom = Column(String)
    to_uom = Column(String)
    ratio = Column(Numeric(18, 4))
