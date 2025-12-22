import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String)
    manager_id = Column(UUID(as_uuid=True), nullable=True)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    employee_code = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    job_title = Column(String)
    base_salary = Column(Numeric(18, 2), default=0)
    is_active = Column(Boolean, default=True)
    joined_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
