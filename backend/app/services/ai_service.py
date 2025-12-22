from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List
import uuid
from ..models.ai_settings import AISettings, AIInsight
from ..models.sales import SalesOrder
from ..models.procurement import PurchaseOrder
from ..models.inventory import Product
from ..models.ledger import StockLedger

class AIService:
    """AI-powered insights with resource-aware toggling"""
    
    @staticmethod
    def is_feature_enabled(db: Session, workspace_id: uuid.UUID, feature: str) -> bool:
        """Check if AI feature is enabled for workspace"""
        settings = db.query(AISettings).filter(
            AISettings.workspace_id == workspace_id
        ).first()
        
        if not settings:
            # Create default settings (all disabled for safety)
            settings = AISettings(
                workspace_id=workspace_id,
                anomaly_detection_enabled=False,
                predictive_analytics_enabled=False,
                smart_recommendations_enabled=False,
                natural_language_query_enabled=False,
                auto_categorization_enabled=False
            )
            db.add(settings)
            db.commit()
            return False
        
        feature_map = {
            "anomaly_detection": settings.anomaly_detection_enabled,
            "predictive_analytics": settings.predictive_analytics_enabled,
            "smart_recommendations": settings.smart_recommendations_enabled,
            "natural_language_query": settings.natural_language_query_enabled,
            "auto_categorization": settings.auto_categorization_enabled
        }
        
        return feature_map.get(feature, False)
    
    @staticmethod
    def detect_anomalies(db: Session, workspace_id: uuid.UUID) -> List[dict]:
        """Detect unusual patterns in transactions (Simple rule-based for now)"""
        if not AIService.is_feature_enabled(db, workspace_id, "anomaly_detection"):
            return {"message": "Anomaly detection is disabled", "anomalies": []}
        
        anomalies = []
        
        # 1. Detect unusually high purchase orders (>3x average)
        avg_po = db.query(func.avg(PurchaseOrder.total_amount)).filter(
            PurchaseOrder.workspace_id == workspace_id
        ).scalar() or 0
        
        high_pos = db.query(PurchaseOrder).filter(
            and_(
                PurchaseOrder.workspace_id == workspace_id,
                PurchaseOrder.total_amount > (avg_po * 3)
            )
        ).limit(5).all()
        
        for po in high_pos:
            anomalies.append({
                "type": "high_purchase_order",
                "severity": "warning",
                "title": f"Unusually high PO: {po.po_number}",
                "description": f"Amount Rp {po.total_amount:,.0f} is 3x above average",
                "data": {"po_id": str(po.id), "amount": float(po.total_amount)}
            })
        
        # 2. Detect duplicate transactions (same vendor, same amount, same day)
        # This would be more complex in production
        
        # 3. Detect unusual sales patterns
        yesterday = datetime.now().date() - timedelta(days=1)
        recent_sales = db.query(SalesOrder).filter(
            and_(
                SalesOrder.workspace_id == workspace_id,
                func.date(SalesOrder.date) == yesterday
            )
        ).count()
        
        avg_daily_sales = 10  # Mock - would calculate from historical data
        
        if recent_sales < (avg_daily_sales * 0.5):
            anomalies.append({
                "type": "low_sales_day",
                "severity": "info",
                "title": "Sales below average yesterday",
                "description": f"Only {recent_sales} orders vs average {avg_daily_sales}",
                "data": {"date": str(yesterday), "count": recent_sales}
            })
        
        return {"message": "Anomaly detection completed", "anomalies": anomalies}
    
    @staticmethod
    def predict_sales(db: Session, workspace_id: uuid.UUID, days_ahead: int = 30) -> dict:
        """Simple sales prediction (Linear trend for demo)"""
        if not AIService.is_feature_enabled(db, workspace_id, "predictive_analytics"):
            return {"message": "Predictive analytics is disabled"}
        
        # Get last 30 days sales
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        
        sales_data = db.query(
            func.date(SalesOrder.date).label('date'),
            func.sum(SalesOrder.total_amount).label('total')
        ).filter(
            and_(
                SalesOrder.workspace_id == workspace_id,
                SalesOrder.date >= thirty_days_ago
            )
        ).group_by(func.date(SalesOrder.date)).all()
        
        if not sales_data:
            return {"message": "Insufficient data for prediction"}
        
        # Simple linear trend (in production, use proper ML)
        total_sales = sum([float(day.total) for day in sales_data])
        avg_daily = total_sales / len(sales_data)
        
        # Mock trend calculation
        trend_direction = "increasing" if len(sales_data) > 15 else "stable"
        predicted_total = avg_daily * days_ahead * 1.05  # 5% growth assumption
        
        return {
            "message": "Sales prediction generated",
            "prediction": {
                "days_ahead": days_ahead,
                "predicted_total": predicted_total,
                "avg_daily": avg_daily,
                "trend": trend_direction,
                "confidence": 0.75  # Mock confidence score
            }
        }
    
    @staticmethod
    def get_smart_recommendations(db: Session, workspace_id: uuid.UUID) -> List[dict]:
        """AI-powered business recommendations"""
        if not AIService.is_feature_enabled(db, workspace_id, "smart_recommendations"):
            return {"message": "Smart recommendations are disabled", "recommendations": []}
        
        recommendations = []
        
        # 1. Low stock alert + reorder recommendation
        low_stock_products = db.query(Product).filter(
            and_(
                Product.workspace_id == workspace_id,
                Product.id.in_(
                    db.query(StockLedger.product_id).filter(
                        StockLedger.workspace_id == workspace_id
                    ).group_by(StockLedger.product_id).having(
                        func.sum(StockLedger.quantity) < 10
                    )
                )
            )
        ).limit(5).all()
        
        for product in low_stock_products:
            recommendations.append({
                "type": "reorder_suggestion",
                "priority": "high",
                "title": f"Reorder {product.name}",
                "description": f"Stock level is low. Recommended reorder quantity: 50 units",
                "action": f"Create PO for {product.code}",
                "data": {"product_id": str(product.id), "suggested_qty": 50}
            })
        
        # 2. Payment optimization
        recommendations.append({
            "type": "payment_optimization",
            "priority": "medium",
            "title": "Optimize payment terms",
            "description": "Consider negotiating 30-day terms with top 3 suppliers for better cash flow",
            "action": "Review supplier contracts",
            "data": {}
        })
        
        # 3. Sales opportunity
        recommendations.append({
            "type": "sales_opportunity",
            "priority": "low",
            "title": "Cross-selling opportunity",
            "description": "Customers who bought Product A often buy Product B. Bundle them?",
            "action": "Create product bundle",
            "data": {}
        })
        
        return {"message": "Recommendations generated", "recommendations": recommendations}
    
    @staticmethod
    def create_insight(
        db: Session,
        workspace_id: uuid.UUID,
        insight_type: str,
        severity: str,
        title: str,
        description: str,
        data: dict = None
    ) -> AIInsight:
        """Save AI insight to database"""
        insight = AIInsight(
            workspace_id=workspace_id,
            insight_type=insight_type,
            severity=severity,
            title=title,
            description=description,
            data=data or {}
        )
        db.add(insight)
        db.commit()
        db.refresh(insight)
        return insight
