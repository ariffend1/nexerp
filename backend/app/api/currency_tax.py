from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..services.currency_service import CurrencyService
from ..services.tax_service import TaxService
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import date

router = APIRouter(prefix="/currency-tax", tags=["currency-tax"])

# ===== CURRENCY ENDPOINTS =====

@router.post("/currencies/seed")
async def seed_currencies(db: Session = Depends(get_db)):
    """Seed common currencies"""
    CurrencyService.seed_currencies(db)
    return {"message": "Currencies seeded successfully"}

@router.post("/exchange-rates/update")
async def update_exchange_rates(
    base_currency: str = "USD",
    db: Session = Depends(get_db)
):
    """Fetch and update exchange rates from API"""
    result = await CurrencyService.update_exchange_rates(db, base_currency)
    return result

@router.get("/exchange-rates/{from_currency}/{to_currency}")
async def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    rate_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get exchange rate for currency pair"""
    date_obj = date.fromisoformat(rate_date) if rate_date else None
    rate = CurrencyService.get_exchange_rate(db, from_currency, to_currency, date_obj)
    
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": float(rate) if rate else None,
        "date": str(date_obj or date.today())
    }

class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    rate_date: Optional[str] = None

@router.post("/convert")
async def convert_currency(
    request: ConvertRequest,
    db: Session = Depends(get_db)
):
    """Convert amount between currencies"""
    date_obj = date.fromisoformat(request.rate_date) if request.rate_date else None
    converted = CurrencyService.convert_amount(
        db,
        Decimal(str(request.amount)),
        request.from_currency,
        request.to_currency,
        date_obj
    )
    
    return {
        "original_amount": request.amount,
        "from_currency": request.from_currency,
        "to_currency": request.to_currency,
        "converted_amount": float(converted) if converted else None,
        "exchange_rate": float(CurrencyService.get_exchange_rate(db, request.from_currency, request.to_currency, date_obj)) if converted else None
    }

# ===== TAX ENDPOINTS =====

@router.post("/tax/seed")
async def seed_tax_rates(
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user)
):
    """Seed Indonesian tax rates"""
    TaxService.seed_tax_rates(db, user.workspace_id)
    return {"message": "Tax rates seeded successfully"}

class PPNRequest(BaseModel):
    amount: float
    include_tax: bool = False

@router.post("/tax/ppn/calculate")
async def calculate_ppn(request: PPNRequest):
    """Calculate PPN (VAT) 11%"""
    result = TaxService.calculate_ppn(Decimal(str(request.amount)), request.include_tax)
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in result.items()}

class PPh21Request(BaseModel):
    annual_income: float
    has_npwp: bool = True

@router.post("/tax/pph21/calculate")
async def calculate_pph_21(request: PPh21Request):
    """Calculate PPh 21 (Income Tax)"""
    result = TaxService.calculate_pph_21(Decimal(str(request.annual_income)), request.has_npwp)
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in result.items()}

class PPh23Request(BaseModel):
    amount: float
    has_npwp: bool = True

@router.post("/tax/pph23/calculate")
async def calculate_pph_23(request: PPh23Request):
    """Calculate PPh 23 (Withholding Tax)"""
    result = TaxService.calculate_pph_23(Decimal(str(request.amount)), request.has_npwp)
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in result.items()}

class PPh42Request(BaseModel):
    amount: float
    service_type: str = "construction"

@router.post("/tax/pph42/calculate")
async def calculate_pph_4_2(request: PPh42Request):
    """Calculate PPh 4(2) (Final Tax)"""
    result = TaxService.calculate_pph_4_2(Decimal(str(request.amount)), request.service_type)
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in result.items()}
