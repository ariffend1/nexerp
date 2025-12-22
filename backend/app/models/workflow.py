import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class WorkflowStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

class WorkflowTrigger(str, enum.Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT = "event"  # On document create/update/delete
    CONDITION = "condition"  # When condition met

class Workflow(Base):
    """Workflow definition"""
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    
    # Workflow config
    trigger_type = Column(String)  # WorkflowTrigger enum
    trigger_config = Column(JSON)  # Trigger-specific configuration
    
    # Visual designer data (node positions, connections)
    flow_data = Column(JSON)  # React Flow compatible format
    
    # Status
    status = Column(String, default=WorkflowStatus.DRAFT.value)
    is_active = Column(Boolean, default=False)
    
    # Stats
    execution_count = Column(Integer, default=0)
    last_executed = Column(DateTime(timezone=True), nullable=True)
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class WorkflowNode(Base):
    """Individual workflow nodes/steps"""
    __tablename__ = "workflow_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"))
    
    node_type = Column(String)  # action, condition, approval, notification
    node_config = Column(JSON)  # Node-specific configuration
    
    # For visual designer
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkflowExecution(Base):
    """Workflow execution history"""
    __tablename__ = "workflow_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    
    # Execution details
    status = Column(String)  # pending, running, completed, failed
    triggered_by = Column(String)  # User ID or "system"
    context_data = Column(JSON)  # Input data for execution
    
    # Results
    execution_log = Column(JSON)  # Step-by-step log
    error_message = Column(Text, nullable=True)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class ApprovalRequest(Base):
    """Approval requests from workflows"""
    __tablename__ = "approval_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    workflow_execution_id = Column(UUID(as_uuid=True), ForeignKey("workflow_executions.id"))
    
    # Approval details
    title = Column(String)
    description = Column(Text)
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Status
    status = Column(String, default="pending")  # pending, approved, rejected
    decision_notes = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
