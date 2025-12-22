from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.excel_service import ExcelService
from ..models.inventory import Product
from ..models.accounting import Partner
import uuid

router = APIRouter(prefix="/import-export", tags=["import-export"])

@router.get("/products/export")
async def export_products(db: Session = Depends(get_db)):
    """Export all products to Excel"""
    products = db.query(Product).all()
    data = [{'code': p.code, 'name': p.name, 'uom': p.uom, 'type': p.type, 'base_price': float(p.base_price)} for p in products]
    
    excel_file = ExcelService.export_to_excel(data, "products.xlsx")
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products.xlsx"}
    )

@router.get("/products/template")
async def get_products_template():
    """Download Excel template for product import"""
    fields = ['code', 'name', 'uom', 'type', 'base_price']
    template = ExcelService.get_template(fields)
    
    return StreamingResponse(
        template,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products_template.xlsx"}
    )

@router.post("/products/import")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import products from Excel"""
    workspace_id = uuid.uuid4()  # Mock
    contents = await file.read()
    
    from io import BytesIO
    result = ExcelService.import_from_excel(BytesIO(contents), Product, db, workspace_id)
    return result

@router.get("/partners/export")
async def export_partners(db: Session = Depends(get_db)):
    """Export all partners to Excel"""
    partners = db.query(Partner).all()
    data = [{'code': p.code, 'name': p.name, 'category': p.category, 'credit_limit': float(p.credit_limit)} for p in partners]
    
    excel_file = ExcelService.export_to_excel(data, "partners.xlsx")
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=partners.xlsx"}
    )
