from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.reporting_service import ReportingService
from ..models.reporting import CustomReport
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid

router = APIRouter(prefix="/reports", tags=["reports"])

class ReportCreate(BaseModel):
    name: str
    category: str
    query_config: dict
    columns: list

@router.get("/templates")
async def get_report_templates():
    """Get pre-built report templates"""
    templates = ReportingService.get_report_templates()
    return {"count": len(templates), "templates": templates}

@router.post("")
async def create_report(
    data: ReportCreate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Create custom report"""
    report = ReportingService.create_report(
        db,
        user.workspace_id,
        data.name,
        data.category,
        data.query_config,
        data.columns,
        user.user_id
    )
    return {
        "id": str(report.id),
        "name": report.name,
        "category": report.category
    }

@router.get("")
async def list_reports(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """List all reports"""
    reports = db.query(CustomReport).filter(
        CustomReport.workspace_id == user.workspace_id
    ).all()
    
    return {
        "count": len(reports),
        "reports": [
            {
                "id": str(r.id),
                "name": r.name,
                "category": r.category,
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ]
    }

@router.get("/{report_id}")
async def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get report details"""
    report = db.query(CustomReport).filter(
        CustomReport.id == uuid.UUID(report_id),
        CustomReport.workspace_id == user.workspace_id
    ).first()
    
    if not report:
        return {"error": "Report not found"}
    
    return {
        "id": str(report.id),
        "name": report.name,
        "category": report.category,
        "query_config": report.query_config,
        "columns": report.columns
    }

@router.post("/{report_id}/execute")
async def execute_report(
    report_id: str,
    parameters: Optional[Dict] = None,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Execute report and return data"""
    data = ReportingService.execute_report(
        db, uuid.UUID(report_id), parameters
    )
    return {
        "report_id": report_id,
        "row_count": len(data),
        "data": data
    }

@router.get("/{report_id}/export/excel")
async def export_excel(
    report_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Export report to Excel"""
    report = db.query(CustomReport).filter(CustomReport.id == uuid.UUID(report_id)).first()
    
    if not report:
        return {"error": "Report not found"}
    
    data = ReportingService.execute_report(db, uuid.UUID(report_id))
    excel_buffer = ReportingService.export_to_excel(data, report.name)
    
    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={report.name}.xlsx"
        }
    )

@router.get("/{report_id}/export/csv")
async def export_csv(
    report_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Export report to CSV"""
    report = db.query(CustomReport).filter(CustomReport.id == uuid.UUID(report_id)).first()
    
    if not report:
        return {"error": "Report not found"}
    
    data = ReportingService.execute_report(db, uuid.UUID(report_id))
    csv_content = ReportingService.export_to_csv(data)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={report.name}.csv"
        }
    )
