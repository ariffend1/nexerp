from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models.sales import SalesOrder
from app.models.procurement import PurchaseOrder
from app.models.manufacturing import JobOrder
from app.models.ledger import StockLedger
from app.models.finance import CashTransaction
from app.models.hr import Employee, Department
from app.models.auth import User
from app.models.accounting import Partner
from app.models.journals import Journal
import uuid

class DashboardAnalytics:
    """Analytics service for role-based executive dashboards"""
    
    @staticmethod
    def get_admin_metrics(db: Session, workspace_id: uuid.UUID):
        """Admin Dashboard: System health and user management metrics"""
        
        total_users = db.query(func.count(User.id)).filter(
            User.workspace_id == workspace_id
        ).scalar() or 0
        
        active_users = db.query(func.count(User.id)).filter(
            User.workspace_id == workspace_id,
            User.is_active == True
        ).scalar() or 0
        
        # API usage (simulated - would come from logs)
        total_requests_today = 1250  # Mock
        
        # Database stats
        total_records = (
            db.query(func.count(SalesOrder.id)).filter(SalesOrder.workspace_id == workspace_id).scalar() +
            db.query(func.count(PurchaseOrder.id)).filter(PurchaseOrder.workspace_id == workspace_id).scalar() +
            db.query(func.count(JobOrder.id)).filter(JobOrder.workspace_id == workspace_id).scalar()
        )
        
        # System alerts
        error_count = 0  # Mock - would come from error logs
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "api_requests_today": total_requests_today,
            "total_records": total_records,
            "error_count": error_count,
            "system_uptime": "99.98%",
            "avg_response_time_ms": 125,
            "storage_used_gb": 2.4
        }
    
    @staticmethod
    def get_manager_metrics(db: Session, workspace_id: uuid.UUID):
        """Manager Dashboard: Operational and team performance"""
        
        # Revenue MTD
        month_start = datetime.now().replace(day=1)
        revenue_mtd = db.query(func.sum(SalesOrder.total_amount)).filter(
            SalesOrder.workspace_id == workspace_id,
            func.date(SalesOrder.date) >= month_start
        ).scalar() or 0
        
        # Active projects
        active_projects = db.query(func.count(JobOrder.id)).filter(
            JobOrder.workspace_id == workspace_id,
            JobOrder.status.in_(['scheduled', 'in_progress'])
        ).scalar() or 0
        
        # Team size
        total_employees = db.query(func.count(Employee.id)).filter(
            Employee.workspace_id == workspace_id,
            Employee.is_active == True
        ).scalar() or 0
        
        # Pending approvals (from notifications or approval_requests)
        pending_approvals = 5  # Mock - would query ApprovalRequest table
        
        # Budget tracking
        budget_allocated = 50000  # Mock
        budget_spent = float(revenue_mtd) * 0.7  # Simulated expenses
        
        return {
            "revenue_mtd": float(revenue_mtd),
            "revenue_ytd": float(revenue_mtd) * 3.2,  # Mock YTD
            "active_projects": active_projects,
            "total_employees": total_employees,
            "pending_approvals": pending_approvals,
            "budget_allocated": budget_allocated,
            "budget_spent": budget_spent,
            "budget_remaining": budget_allocated - budget_spent,
            "productivity_score": 87.5  # Mock
        }
    
    @staticmethod
    def get_supervisor_metrics(db: Session, workspace_id: uuid.UUID):
        """Supervisor Dashboard: Daily operations and team coordination"""
        
        today = datetime.now().date()
        
        # Production output today
        production_today = db.query(func.count(JobOrder.id)).filter(
            JobOrder.workspace_id == workspace_id,
            func.date(JobOrder.completion_date) == today
        ).scalar() or 0
        
        # Team attendance
        team_size = db.query(func.count(Employee.id)).filter(
            Employee.workspace_id == workspace_id,
            Employee.is_active == True
        ).scalar() or 0
        
        attendance_today = int(team_size * 0.92)  # Mock 92% attendance
        
        # Pending work orders
        pending_work_orders = db.query(func.count(JobOrder.id)).filter(
            JobOrder.workspace_id == workspace_id,
            JobOrder.status == 'scheduled'
        ).scalar() or 0
        
        # Low stock items
        low_stock_count = 3  # Mock - would query inventory with reorder point logic
        
        # Quality metrics
        defect_rate = 1.2  # Mock percentage
        
        return {
            "production_today": production_today,
            "production_target": 50,  # Mock target
            "team_attendance": attendance_today,
            "team_size": team_size,
            "pending_work_orders": pending_work_orders,
            "low_stock_items": low_stock_count,
            "defect_rate": defect_rate,
            "on_time_delivery_rate": 94.5  # Mock
        }
    
    @staticmethod
    def get_gm_metrics(db: Session, workspace_id: uuid.UUID):
        """GM Dashboard: Strategic overview and business health"""
        
        # Monthly revenue trend (last 6 months)
        revenue_6m = {}
        for i in range(6):
            month_date = (datetime.now() - timedelta(days=30*i)).replace(day=1)
            month_revenue = db.query(func.sum(SalesOrder.total_amount)).filter(
                SalesOrder.workspace_id == workspace_id,
                extract('month', SalesOrder.date) == month_date.month,
                extract('year', SalesOrder.date) == month_date.year
            ).scalar() or 0
            revenue_6m[month_date.strftime("%b")] = float(month_revenue)
        
        # Gross profit margin
        total_revenue = sum(revenue_6m.values())
        total_cogs = total_revenue * 0.65  # Mock COGS at 65%
        gross_profit = total_revenue - total_cogs
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Operating cash flow
        cash_in = db.query(func.sum(CashTransaction.amount)).filter(
            CashTransaction.workspace_id == workspace_id,
            CashTransaction.transaction_type == 'receipt'
        ).scalar() or 0
        
        cash_out = db.query(func.sum(CashTransaction.amount)).filter(
            CashTransaction.workspace_id == workspace_id,
            CashTransaction.transaction_type == 'payment'
        ).scalar() or 0
        
        return {
            "monthly_revenue": revenue_6m,
            "total_revenue_6m": total_revenue,
            "gross_profit_margin": round(gross_margin, 2),
            "operating_cash_flow": float(cash_in - cash_out),
            "customer_count": db.query(func.count(Partner.id)).filter(
                Partner.workspace_id == workspace_id,
                Partner.category.in_(['customer', 'both'])
            ).scalar() or 0,
            "employee_turnover_rate": 3.2,  # Mock
            "market_share": 12.5  # Mock
        }
    
    @staticmethod
    def get_direksi_metrics(db: Session, workspace_id: uuid.UUID):
        """Direksi Dashboard: Executive summary and financial health"""
        
        # Get current year revenue
        current_year = datetime.now().year
        revenue_current = db.query(func.sum(SalesOrder.total_amount)).filter(
            SalesOrder.workspace_id == workspace_id,
            extract('year', SalesOrder.date) == current_year
        ).scalar() or 0
        
        # Previous year (mock)
        revenue_previous = float(revenue_current) * 0.85  # Mock 15% growth YoY
        
        yoy_growth = ((revenue_current - revenue_previous) / revenue_previous * 100) if revenue_previous > 0 else 0
        
        # Financial ratios
        net_profit = float(revenue_current) * 0.18  # Mock 18% net margin
        total_assets = float(revenue_current) * 1.5  # Mock
        total_equity = total_assets * 0.6  # Mock
        total_debt = total_assets - total_equity
        
        return {
            "revenue_current_year": float(revenue_current),
            "revenue_previous_year": revenue_previous,
            "yoy_growth_percent": round(yoy_growth, 2),
            "net_profit": net_profit,
            "net_profit_margin": 18.0,  # Mock
            "roi_percent": 22.5,  # Mock
            "total_assets": total_assets,
            "total_equity": total_equity,
            "debt_to_equity_ratio": round(total_debt / total_equity, 2) if total_equity > 0 else 0,
            "asset_turnover_ratio": round(revenue_current / total_assets, 2) if total_assets > 0 else 0,
            "strategic_initiatives_progress": 78.5  # Mock percentage
        }
