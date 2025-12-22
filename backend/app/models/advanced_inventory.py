import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class SerialNumber(Base):
    """Individual item tracking with serial numbers"""
    __tablename__ = "serial_numbers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    serial_number = Column(String, unique=True, index=True)
    status = Column(String, default="available")  # available, reserved, sold, scrapped
    
    # Location tracking
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)
    location = Column(String, nullable=True)
    
    # Transaction history
    received_date = Column(Date, nullable=True)
    sold_date = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BatchLot(Base):
    """Batch/Lot management with expiry tracking"""
    __tablename__ = "batch_lots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    batch_number = Column(String, index=True)
    lot_number = Column(String, nullable=True)
    
    # Quantity tracking
    quantity_total = Column(Integer)
    quantity_available = Column(Integer)
    
    # Dates
    manufacturing_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    
    # Location
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BarcodeMapping(Base):
    """Barcode to product mapping"""
    __tablename__ = "barcode_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    barcode = Column(String, unique=True, index=True)
    barcode_type = Column(String, default="ean13")  # ean13, code128, qr
    
    is_primary = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StockReorderRule(Base):
    """Min/Max automatic reorder rules"""
    __tablename__ = "stock_reorder_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    
    min_quantity = Column(Integer)
    max_quantity = Column(Integer)
    reorder_quantity = Column(Integer)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
