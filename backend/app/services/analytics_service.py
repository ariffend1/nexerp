from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models.sales import SalesOrder
from app.models.procurement import PurchaseOrder
from app.models.manufacturing import JobOrder
from app.models.ledger import StockLedger
from app.models.finance import CashTransaction
import uuid

class AnalyticsService:
    @staticmethod
    def get_dashboard_kpis(db: Session, workspace_id: uuid.UUID):
        """Get key KPIs for dashboard overview"""
        
        today = datetime.now().date()
        month_start = today.replace(day=1)
        
        # Sales metrics
        total_sales = db.query(func.sum(SalesOrder.total_amount)).filter(
            SalesOrder.workspace_id == workspace_id,
            func.date(SalesOrder.date) >= month_start
        ).scalar() or 0
        
        # Procurement metrics
        total_procurement = db.query(func.sum(PurchaseOrder.total_amount)).filter(
            PurchaseOrder.workspace_id == workspace_id,
            func.date(PurchaseOrder.date) >= month_start
        ).scalar() or 0
        
        # Job orders
        active_jobs = db.query(func.count(JobOrder.id)).filter(
            JobOrder.workspace_id == workspace_id,
            JobOrder.status.in_(['scheduled', 'in_progress'])
        ).scalar() or 0
        
        # Cash flow
        cash_in = db.query(func.sum(CashTransaction.amount)).filter(
            CashTransaction.workspace_id == workspace_id,
            CashTransaction.transaction_type == 'receipt',
            func.date(CashTransaction.transaction_date) >= month_start
        ).scalar() or 0
        
        cash_out = db.query(func.sum(CashTransaction.amount)).filter(
            CashTransaction.workspace_id == workspace_id,
            CashTransaction.transaction_type == 'payment',
            func.date(CashTransaction.transaction_date) >= month_start
        ).scalar() or 0
        
        return {
            'total_sales': float(total_sales),
            'total_procurement': float(total_procurement),
            'active_jobs': active_jobs,
            'cash_in': float(cash_in),
            'cash_out': float(cash_out),
            'net_cash_flow': float(cash_in - cash_out)
        }
    
    @staticmethod
    def get_sales_trend(db: Session, workspace_id: uuid.UUID, days: int = 30):
        """Get daily sales trend for charts"""
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        sales_by_day = db.query(
            func.date(SalesOrder.date).label('date'),
            func.sum(SalesOrder.total_amount).label('amount')
        ).filter(
            SalesOrder.workspace_id == workspace_id,
            func.date(SalesOrder.date) >= start_date
        ).group_by(func.date(SalesOrder.date)).all()
        
        return [{'date': str(s.date), 'amount': float(s.amount)} for s in sales_by_day]
    
    @staticmethod
    def get_top_products(db: Session, workspace_id: uuid.UUID, limit: int = 10):
        """Get top selling products"""
        from app.models.sales import SOLine
        from app.models.inventory import Product
        
        top_products = db.query(
            Product.name,
            func.sum(SOLine.qty * SOLine.unit_price).label('revenue')
        ).join(SOLine, SOLine.product_id == Product.id).filter(
            Product.workspace_id == workspace_id
        ).group_by(Product.name).order_by(func.sum(SOLine.qty * SOLine.unit_price).desc()).limit(limit).all()
        
        return [{'product': p.name, 'revenue': float(p.revenue)} for p in top_products]
