from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.dashboard_analytics import DashboardAnalytics
from ..models.rbac import UserRole

router = APIRouter(prefix="/dashboards", tags=["dashboards"])

@router.get("/admin")
async def get_admin_dashboard(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get Admin dashboard metrics"""
    metrics = DashboardAnalytics.get_admin_metrics(db, user.workspace_id)
    return {
        "role": "admin",
        "metrics": metrics,
        "last_updated": "2025-12-20T21:45:00Z"
    }

@router.get("/manager")
async def get_manager_dashboard(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get Manager dashboard metrics"""
    metrics = DashboardAnalytics.get_manager_metrics(db, user.workspace_id)
    return {
        "role": "manager",
        "metrics": metrics,
        "last_updated": "2025-12-20T21:45:00Z"
    }

@router.get("/supervisor")
async def get_supervisor_dashboard(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get Supervisor dashboard metrics"""
    metrics = DashboardAnalytics.get_supervisor_metrics(db, user.workspace_id)
    return {
        "role": "supervisor",
        "metrics": metrics,
        "last_updated": "2025-12-20T21:45:00Z"
    }

@router.get("/gm")
async def get_gm_dashboard(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get GM dashboard metrics"""
    metrics = DashboardAnalytics.get_gm_metrics(db, user.workspace_id)
    return {
        "role": "gm",
        "metrics": metrics,
        "last_updated": "2025-12-20T21:45:00Z"
    }

@router.get("/direksi")
async def get_direksi_dashboard(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get Direksi dashboard metrics"""
    metrics = DashboardAnalytics.get_direksi_metrics(db, user.workspace_id)
    return {
        "role": "direksi",
        "metrics": metrics,
        "last_updated": "2025-12-20T21:45:00Z"
    }
