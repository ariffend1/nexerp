from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.reporting import CustomReport, ScheduledReport, ReportExecution
from typing import List, Dict, Optional
import uuid
import pandas as pd
from io import BytesIO
import csv

class ReportingService:
    """Advanced reporting service"""
    
    @staticmethod
    def create_report(
        db: Session,
        workspace_id: uuid.UUID,
        name: str,
        category: str,
        query_config: dict,
        columns: list,
        created_by: uuid.UUID
    ) -> CustomReport:
        """Create custom report"""
        report = CustomReport(
            workspace_id=workspace_id,
            name=name,
            category=category,
            query_config=query_config,
            columns=columns,
            filters={},
            created_by=created_by
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    
    @staticmethod
    def execute_report(
        db: Session,
        report_id: uuid.UUID,
        parameters: Dict = None
    ) -> List[Dict]:
        """Execute report and return results"""
        report = db.query(CustomReport).filter(CustomReport.id == report_id).first()
        
        if not report:
            return []
        
        # Build query based on report config
        query_config = report.query_config
        table = query_config.get("table")
        fields = query_config.get("fields", ["*"])
        conditions = query_config.get("conditions", [])
        
        # Build SQL (simplified - in production use query builder)
        if not table:
            return []
        
        sql = f"SELECT {', '.join(fields)} FROM {table}"
        
        # Apply conditions
        if conditions:
            where_clauses = []
            for condition in conditions:
                field = condition.get("field")
                operator = condition.get("operator", "=")
                value = condition.get("value")
                where_clauses.append(f"{field} {operator} '{value}'")
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
        
        # Apply filters from report
        if report.filters:
            # Apply additional filters
            pass
        
        # Execute query
        try:
            result = db.execute(text(sql))
            rows = result.fetchall()
            
            # Convert to list of dicts
            data = []
            for row in rows:
                data.append(dict(row._mapping))
            
            return data
        except Exception as e:
            print(f"Error executing report: {e}")
            return []
    
    @staticmethod
    def export_to_excel(data: List[Dict], report_name: str) -> BytesIO:
        """Export report data to Excel"""
        df = pd.DataFrame(data)
        
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=report_name[:30], index=False)
        
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def export_to_csv(data: List[Dict]) -> str:
        """Export report data to CSV"""
        if not data:
            return ""
        
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue().decode('utf-8')
    
    @staticmethod
    def get_report_templates() -> List[Dict]:
        """Get pre-built report templates"""
        return [
            {
                "id": "sales_summary",
                "name": "Sales Summary Report",
                "category": "sales",
                "description": "Daily/monthly sales performance",
                "query_config": {
                    "table": "sales_orders",
                    "fields": ["so_number", "date", "customer_id", "total_amount", "status"],
                    "conditions": []
                },
                "columns": [
                    {"key": "so_number", "label": "SO Number", "type": "string"},
                    {"key": "date", "label": "Date", "type": "date"},
                    {"key": "total_amount", "label": "Amount", "type": "currency"},
                    {"key": "status", "label": "Status", "type": "string"}
                ]
            },
            {
                "id": "inventory_valuation",
                "name": "Inventory Valuation",
                "category": "inventory",
                "description": "Stock value by product",
                "query_config": {
                    "table": "products",
                    "fields": ["code", "name", "type"],
                    "conditions": []
                },
                "columns": [
                    {"key": "code", "label": "Product Code", "type": "string"},
                    {"key": "name", "label": "Product Name", "type": "string"},
                    {"key": "quantity", "label": "Quantity", "type": "number"},
                    {"key": "value", "label": "Total Value", "type": "currency"}
                ]
            },
            {
                "id": "aging_receivables",
                "name": "Accounts Receivable Aging",
                "category": "finance",
                "description": "Outstanding invoices by age",
                "query_config": {
                    "table": "sales_orders",
                    "fields": ["customer_id", "so_number", "total_amount", "date"],
                    "conditions": [{"field": "status", "operator": "=", "value": "invoiced"}]
                },
                "columns": [
                    {"key": "customer", "label": "Customer", "type": "string"},
                    {"key": "invoice", "label": "Invoice", "type": "string"},
                    {"key": "amount", "label": "Amount", "type": "currency"},
                    {"key": "days_overdue", "label": "Days Overdue", "type": "number"}
                ]
            },
            {
                "id": "production_efficiency",
                "name": "Production Efficiency",
                "category": "manufacturing",
                "description": "Manufacturing performance KPIs",
                "query_config": {
                    "table": "spks",
                    "fields": ["spk_number", "product_id", "quantity_target", "quantity_actual", "status"],
                    "conditions": []
                },
                "columns": [
                    {"key": "spk_number", "label": "SPK", "type": "string"},
                    {"key": "product", "label": "Product", "type": "string"},
                    {"key": "efficiency", "label": "Efficiency %", "type": "percentage"},
                    {"key": "status", "label": "Status", "type": "string"}
                ]
            }
        ]
