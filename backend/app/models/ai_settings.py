import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class AISettings(Base):
    """Workspace-level AI feature configuration"""
    __tablename__ = "ai_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), unique=True)
    
    # Feature toggles
    anomaly_detection_enabled = Column(Boolean, default=False)
    predictive_analytics_enabled = Column(Boolean, default=False)
    smart_recommendations_enabled = Column(Boolean, default=False)
    natural_language_query_enabled = Column(Boolean, default=False)
    auto_categorization_enabled = Column(Boolean, default=False)
    
    # Advanced settings
    ai_model_preference = Column(String, default="standard")  # standard, advanced, custom
    max_ai_calls_per_day = Column(Integer, default=100)  # Rate limiting
    
    # Metadata
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIInsight(Base):
    """AI-generated insights and recommendations"""
    __tablename__ = "ai_insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    
    insight_type = Column(String)  # 'anomaly', 'prediction', 'recommendation'
    severity = Column(String)  # 'info', 'warning', 'critical'
    title = Column(String)
    description = Column(String)
    data = Column(JSON)  # Additional context data
    
    is_read = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
