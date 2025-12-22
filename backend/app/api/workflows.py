from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.workflow_service import WorkflowEngine
from ..models.workflow import Workflow, WorkflowExecution
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

router = APIRouter(prefix="/workflows", tags=["workflows"])

class WorkflowCreate(BaseModel):
    name: str
    description: str
    trigger_type: str = "manual"

class FlowDataUpdate(BaseModel):
    flow_data: dict

@router.get("/templates")
async def get_workflow_templates():
    """Get pre-built workflow templates"""
    templates = WorkflowEngine.get_workflow_templates()
    return {"count": len(templates), "templates": templates}

@router.post("")
async def create_workflow(
    data: WorkflowCreate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Create new workflow"""
    workflow = WorkflowEngine.create_workflow(
        db,
        user.workspace_id,
        data.name,
        data.description,
        data.trigger_type,
        user.user_id
    )
    return {
        "id": str(workflow.id),
        "name": workflow.name,
        "status": workflow.status
    }

@router.get("")
async def list_workflows(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """List all workflows"""
    workflows = db.query(Workflow).filter(
        Workflow.workspace_id == user.workspace_id
    ).all()
    
    return {
        "count": len(workflows),
        "workflows": [
            {
                "id": str(w.id),
                "name": w.name,
                "status": w.status,
                "is_active": w.is_active,
                "execution_count": w.execution_count,
                "last_executed": w.last_executed.isoformat() if w.last_executed else None
            }
            for w in workflows
        ]
    }

@router.get("/{workflow_id}")
async def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get workflow details"""
    workflow = db.query(Workflow).filter(
        Workflow.id == uuid.UUID(workflow_id),
        Workflow.workspace_id == user.workspace_id
    ).first()
    
    if not workflow:
        return {"error": "Workflow not found"}
    
    return {
        "id": str(workflow.id),
        "name": workflow.name,
        "description": workflow.description,
        "trigger_type": workflow.trigger_type,
        "status": workflow.status,
        "is_active": workflow.is_active,
        "flow_data": workflow.flow_data,
        "execution_count": workflow.execution_count
    }

@router.put("/{workflow_id}/flow")
async def update_flow_data(
    workflow_id: str,
    data: FlowDataUpdate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Update visual workflow design"""
    success = WorkflowEngine.update_flow_data(
        db, uuid.UUID(workflow_id), data.flow_data
    )
    return {"success": success}

@router.post("/{workflow_id}/activate")
async def activate_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Activate workflow"""
    success = WorkflowEngine.activate_workflow(db, uuid.UUID(workflow_id))
    return {"success": success, "message": "Workflow activated"}

@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    context_data: Optional[Dict] = None,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Execute workflow manually"""
    execution = await WorkflowEngine.execute_workflow(
        db,
        uuid.UUID(workflow_id),
        str(user.user_id),
        context_data
    )
    return {
        "execution_id": str(execution.id),
        "status": execution.status,
        "started_at": execution.started_at.isoformat()
    }

@router.get("/{workflow_id}/executions")
async def get_workflow_executions(
    workflow_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get workflow execution history"""
    executions = db.query(WorkflowExecution).filter(
        WorkflowExecution.workflow_id == uuid.UUID(workflow_id)
    ).order_by(WorkflowExecution.started_at.desc()).limit(50).all()
    
    return {
        "count": len(executions),
        "executions": [
            {
                "id": str(e.id),
                "status": e.status,
                "started_at": e.started_at.isoformat(),
                "completed_at": e.completed_at.isoformat() if e.completed_at else None,
                "error_message": e.error_message
            }
            for e in executions
        ]
    }
