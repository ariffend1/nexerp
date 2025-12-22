import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    GM = "gm"
    DIREKSI = "direksi"
    EMPLOYEE = "employee"  # Default role

# Many-to-Many association table for Role-Permission
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'))
)

# Many-to-Many association table for User-Role
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    name = Column(String, unique=True, index=True)
    description = Column(String)
    is_system_role = Column(Boolean, default=False)  # True for Admin, Manager, Employee
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, index=True)  # e.g., 'inventory.view', 'procurement.approve'
    module = Column(String)  # 'inventory', 'procurement', 'sales', etc.
    action = Column(String)  # 'view', 'create', 'edit', 'delete', 'approve'
    description = Column(String)
