from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.workflow import Workflow, WorkflowNode, WorkflowExecution, ApprovalRequest
from typing import Dict, List, Optional
import uuid
import json

class WorkflowEngine:
    """Workflow execution engine"""
    
    @staticmethod
    def create_workflow(
        db: Session,
        workspace_id: uuid.UUID,
        name: str,
        description: str,
        trigger_type: str,
        created_by: uuid.UUID
    ) -> Workflow:
        """Create new workflow"""
        workflow = Workflow(
            workspace_id=workspace_id,
            name=name,
            description=description,
            trigger_type=trigger_type,
            trigger_config={},
            flow_data={"nodes": [], "edges": []},
            created_by=created_by,
            status="draft"
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return workflow
    
    @staticmethod
    def update_flow_data(
        db: Session,
        workflow_id: uuid.UUID,
        flow_data: dict
    ):
        """Update visual workflow design"""
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if workflow:
            workflow.flow_data = flow_data
            db.commit()
            return True
        return False
    
    @staticmethod
    def activate_workflow(db: Session, workflow_id: uuid.UUID):
        """Activate workflow for execution"""
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if workflow:
            workflow.status = "active"
            workflow.is_active = True
            db.commit()
            return True
        return False
    
    @staticmethod
    async def execute_workflow(
        db: Session,
        workflow_id: uuid.UUID,
        triggered_by: str,
        context_data: Dict = None
    ) -> WorkflowExecution:
        """Execute workflow (simplified version)"""
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow or not workflow.is_active:
            raise ValueError("Workflow not found or inactive")
        
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            workspace_id=workflow.workspace_id,
            status="running",
            triggered_by=triggered_by,
            context_data=context_data or {}
        )
        db.add(execution)
        db.commit()
        
        # Execute nodes (simplified - in production use Celery/background tasks)
        execution_log = []
        flow_data = workflow.flow_data
        nodes = flow_data.get("nodes", [])
        
        try:
            for node in nodes:
                node_type = node.get("type")
                node_data = node.get("data", {})
                
                # Execute based on node type
                if node_type == "action":
                    action_result = WorkflowEngine._execute_action(db, node_data, context_data)
                    execution_log.append({
                        "node_id": node.get("id"),
                        "type": "action",
                        "result": action_result,
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif node_type == "condition":
                    condition_result = WorkflowEngine._evaluate_condition(node_data, context_data)
                    execution_log.append({
                        "node_id": node.get("id"),
                        "type": "condition",
                        "result": condition_result,
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif node_type == "notification":
                    WorkflowEngine._send_notification(db, node_data)
                    execution_log.append({
                        "node_id": node.get("id"),
                        "type": "notification",
                        "result": "sent",
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Mark as completed
            execution.status = "completed"
            execution.execution_log = execution_log
            execution.completed_at = datetime.now()
            
            # Update workflow stats
            workflow.execution_count += 1
            workflow.last_executed = datetime.now()
            
        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
        
        db.commit()
        db.refresh(execution)
        return execution
    
    @staticmethod
    def _execute_action(db: Session, node_data: dict, context: dict) -> str:
        """Execute action node (mock implementation)"""
        action_type = node_data.get("action_type")
        
        if action_type == "update_field":
            # Update document field
            return "field_updated"
        elif action_type == "send_email":
            # Send email
            return "email_sent"
        elif action_type == "create_document":
            # Create document
            return "document_created"
        
        return "action_executed"
    
    @staticmethod
    def _evaluate_condition(node_data: dict, context: dict) -> bool:
        """Evaluate condition node (mock)"""
        condition = node_data.get("condition")
        # Simple condition evaluation
        return True  # Mock
    
    @staticmethod
    def _send_notification(db: Session, node_data: dict):
        """Send notification (mock)"""
        # Would integrate with notification service
        pass
    
    @staticmethod
    def get_workflow_templates() -> List[dict]:
        """Get pre-built workflow templates"""
        return [
            {
                "id": "purchase_approval",
                "name": "Purchase Order Approval",
                "description": "Auto-approve PO below threshold, require approval above",
                "category": "procurement",
                "template_data": {
                    "nodes": [
                        {
                            "id": "1",
                            "type": "trigger",
                            "data": {"label": "PO Created"},
                            "position": {"x": 100, "y": 100}
                        },
                        {
                            "id": "2",
                            "type": "condition",
                            "data": {"label": "Amount > 10M?"},
                            "position": {"x": 300, "y": 100}
                        },
                        {
                            "id": "3",
                            "type": "approval",
                            "data": {"label": "Manager Approval"},
                            "position": {"x": 500, "y": 50}
                        },
                        {
                            "id": "4",
                            "type": "action",
                            "data": {"label": "Auto-approve"},
                            "position": {"x": 500, "y": 150}
                        }
                    ],
                    "edges": [
                        {"id": "e1-2", "source": "1", "target": "2"},
                        {"id": "e2-3", "source": "2", "target": "3", "label": "Yes"},
                        {"id": "e2-4", "source": "2", "target": "4", "label": "No"}
                    ]
                }
            },
            {
                "id": "low_stock_alert",
                "name": "Low Stock Auto-Reorder",
                "description": "Alert when stock low, create draft PO",
                "category": "inventory",
                "template_data": {}
            },
            {
                "id": "invoice_reminder",
                "name": "Invoice Payment Reminder",
                "description": "Send reminder 3 days before due date",
                "category": "finance",
                "template_data": {}
            }
        ]
