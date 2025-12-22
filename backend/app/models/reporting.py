import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class CustomReport(Base):
    """User-defined custom reports"""
    __tablename__ = "custom_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    category = Column(String)  # sales, finance, inventory, manufacturing
    
    # Report definition (SQL-like query or filter config)
    query_config = Column(JSON)
    
    # Display settings
    columns = Column(JSON)  # Column definitions
    filters = Column(JSON)  # Applied filters
    sorting = Column(JSON, nullable=True)  # Sort order
    grouping = Column(JSON, nullable=True)  # Group by fields
    
    # Permissions
    is_public = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ScheduledReport(Base):
    """Scheduled report execution"""
    __tablename__ = "scheduled_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    report_id = Column(UUID(as_uuid=True), ForeignKey("custom_reports.id"))
    
    # Schedule config
    schedule_type = Column(String)  # daily, weekly, monthly
    schedule_config = Column(JSON)  # Day of week, time, etc.
    
    # Recipients
    recipients = Column(JSON)  # List of email addresses
    export_format = Column(String, default="pdf")  # pdf, excel, csv
    
    # Status
    is_active = Column(Boolean, default=True)
    last_sent = Column(DateTime(timezone=True), nullable=True)
    next_run = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ReportExecution(Base):
    """Report execution history"""
    __tablename__ = "report_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    report_id = Column(UUID(as_uuid=True), ForeignKey("custom_reports.id"))
    
    # Execution details
    executed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    parameters = Column(JSON, nullable=True)  # Runtime parameters
    
    # Results
    row_count = Column(Integer, default=0)
    export_format = Column(String, nullable=True)
    file_path = Column(String, nullable=True)  # S3 or local path
    
    status = Column(String)  # completed, failed
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
