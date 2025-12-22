from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.analytics_service import AnalyticsService
import uuid

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard-kpis")
async def get_dashboard_kpis(db: Session = Depends(get_db), user: AuthUser = Depends(get_current_user)):
    return AnalyticsService.get_dashboard_kpis(db, user.workspace_id)

@router.get("/sales-trend")
async def get_sales_trend(days: int = 30, db: Session = Depends(get_db), user: AuthUser = Depends(get_current_user)):
    return AnalyticsService.get_sales_trend(db, user.workspace_id, days)

@router.get("/top-products")
async def get_top_products(limit: int = 10, db: Session = Depends(get_db), user: AuthUser = Depends(get_current_user)):
    return AnalyticsService.get_top_products(db, user.workspace_id, limit)
