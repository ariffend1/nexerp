from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, AuthUser
from app.services.ai_service import AIService
from app.models.ai_settings import AISettings
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai"])

# ===== SETTINGS ENDPOINTS =====

class AISettingsUpdate(BaseModel):
    anomaly_detection_enabled: bool = False
    predictive_analytics_enabled: bool = False
    smart_recommendations_enabled: bool = False
    natural_language_query_enabled: bool = False
    auto_categorization_enabled: bool = False
    max_ai_calls_per_day: int = 100

@router.get("/settings")
async def get_ai_settings(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get current AI settings for workspace"""
    settings = db.query(AISettings).filter(
        AISettings.workspace_id == user.workspace_id
    ).first()
    
    if not settings:
        # Create default (all disabled)
        settings = AISettings(
            workspace_id=user.workspace_id,
            anomaly_detection_enabled=False,
            predictive_analytics_enabled=False,
            smart_recommendations_enabled=False,
            natural_language_query_enabled=False,
            auto_categorization_enabled=False
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return {
        "anomaly_detection_enabled": settings.anomaly_detection_enabled,
        "predictive_analytics_enabled": settings.predictive_analytics_enabled,
        "smart_recommendations_enabled": settings.smart_recommendations_enabled,
        "natural_language_query_enabled": settings.natural_language_query_enabled,
        "auto_categorization_enabled": settings.auto_categorization_enabled,
        "ai_model_preference": settings.ai_model_preference,
        "max_ai_calls_per_day": settings.max_ai_calls_per_day
    }

@router.put("/settings")
async def update_ai_settings(
    settings_update: AISettingsUpdate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Update AI feature toggles"""
    settings = db.query(AISettings).filter(
        AISettings.workspace_id == user.workspace_id
    ).first()
    
    if not settings:
        settings = AISettings(workspace_id=user.workspace_id)
        db.add(settings)
    
    # Update toggles
    settings.anomaly_detection_enabled = settings_update.anomaly_detection_enabled
    settings.predictive_analytics_enabled = settings_update.predictive_analytics_enabled
    settings.smart_recommendations_enabled = settings_update.smart_recommendations_enabled
    settings.natural_language_query_enabled = settings_update.natural_language_query_enabled
    settings.auto_categorization_enabled = settings_update.auto_categorization_enabled
    settings.max_ai_calls_per_day = settings_update.max_ai_calls_per_day
    
    db.commit()
    db.refresh(settings)
    
    return {
        "message": "AI settings updated successfully",
        "settings": {
            "anomaly_detection_enabled": settings.anomaly_detection_enabled,
            "predictive_analytics_enabled": settings.predictive_analytics_enabled,
            "smart_recommendations_enabled": settings.smart_recommendations_enabled,
            "natural_language_query_enabled": settings.natural_language_query_enabled,
            "auto_categorization_enabled": settings.auto_categorization_enabled
        }
    }

# ===== AI INSIGHTS ENDPOINTS =====

@router.get("/anomalies/detect")
async def detect_anomalies(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Run anomaly detection (if enabled)"""
    result = AIService.detect_anomalies(db, user.workspace_id)
    return result

@router.get("/predictions/sales")
async def predict_sales(
    days_ahead: int = 30,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Generate sales prediction (if enabled)"""
    result = AIService.predict_sales(db, user.workspace_id, days_ahead)
    return result

@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get smart business recommendations (if enabled)"""
    result = AIService.get_smart_recommendations(db, user.workspace_id)
    return result

@router.get("/insights")
async def get_ai_insights(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Get all AI-generated insights"""
    from app.models.ai_settings import AIInsight
    
    insights = db.query(AIInsight).filter(
        AIInsight.workspace_id == user.workspace_id,
        AIInsight.is_dismissed == False
    ).order_by(AIInsight.created_at.desc()).limit(20).all()
    
    return {
        "count": len(insights),
        "insights": [
            {
                "id": str(insight.id),
                "type": insight.insight_type,
                "severity": insight.severity,
                "title": insight.title,
                "description": insight.description,
                "is_read": insight.is_read,
                "created_at": insight.created_at.isoformat()
            }
            for insight in insights
        ]
    }
