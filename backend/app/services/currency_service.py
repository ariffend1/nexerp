from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from decimal import Decimal
from app.models.currency_tax import Currency, ExchangeRate
import uuid
import httpx
from typing import Optional

class CurrencyService:
    """Service for currency management and exchange rates"""
    
    # Free API for exchange rates (replace with paid API in production)
    EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"
    
    @staticmethod
    def seed_currencies(db: Session):
        """Seed common currencies"""
        common_currencies = [
            {"code": "IDR", "name": "Indonesian Rupiah", "symbol": "Rp", "decimal_places": 0},
            {"code": "USD", "name": "US Dollar", "symbol": "$", "decimal_places": 2},
            {"code": "EUR", "name": "Euro", "symbol": "€", "decimal_places": 2},
            {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$", "decimal_places": 2},
            {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥", "decimal_places": 2},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥", "decimal_places": 0},
            {"code": "AUD", "name": "Australian Dollar", "symbol": "A$", "decimal_places": 2},
            {"code": "GBP", "name": "British Pound", "symbol": "£", "decimal_places": 2},
        ]
        
        for curr_data in common_currencies:
            existing = db.query(Currency).filter(Currency.code == curr_data["code"]).first()
            if not existing:
                currency = Currency(**curr_data)
                db.add(currency)
        
        db.commit()
    
    @staticmethod
    async def fetch_exchange_rates(base_currency: str = "USD"):
        """Fetch latest exchange rates from API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    CurrencyService.EXCHANGE_API_URL.format(base=base_currency),
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("rates", {})
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return None
    
    @staticmethod
    async def update_exchange_rates(db: Session, base_currency: str = "USD"):
        """Update exchange rates in database"""
        rates = await CurrencyService.fetch_exchange_rates(base_currency)
        if not rates:
            return {"error": "Failed to fetch rates"}
        
        today = date.today()
        updated_count = 0
        
        for to_currency, rate in rates.items():
            # Check if rate already exists for today
            existing = db.query(ExchangeRate).filter(
                and_(
                    ExchangeRate.from_currency_code == base_currency,
                    ExchangeRate.to_currency_code == to_currency,
                    ExchangeRate.rate_date == today
                )
            ).first()
            
            if not existing:
                exchange_rate = ExchangeRate(
                    from_currency_code=base_currency,
                    to_currency_code=to_currency,
                    rate=Decimal(str(rate)),
                    rate_date=today,
                    source="api_exchangerate"
                )
                db.add(exchange_rate)
                updated_count += 1
        
        db.commit()
        return {"message": f"Updated {updated_count} exchange rates", "date": str(today)}
    
    @staticmethod
    def get_exchange_rate(
        db: Session,
        from_currency: str,
        to_currency: str,
        rate_date: Optional[date] = None
    ) -> Optional[Decimal]:
        """Get exchange rate for a specific date (defaults to today)"""
        if from_currency == to_currency:
            return Decimal("1.0")
        
        if rate_date is None:
            rate_date = date.today()
        
        # Try exact date first
        rate_record = db.query(ExchangeRate).filter(
            and_(
                ExchangeRate.from_currency_code == from_currency,
                ExchangeRate.to_currency_code == to_currency,
                ExchangeRate.rate_date == rate_date
            )
        ).first()
        
        if rate_record:
            return rate_record.rate
        
        # Try reverse rate
        reverse_rate = db.query(ExchangeRate).filter(
            and_(
                ExchangeRate.from_currency_code == to_currency,
                ExchangeRate.to_currency_code == from_currency,
                ExchangeRate.rate_date == rate_date
            )
        ).first()
        
        if reverse_rate:
            return Decimal("1.0") / reverse_rate.rate
        
        # Fall back to most recent rate
        latest_rate = db.query(ExchangeRate).filter(
            and_(
                ExchangeRate.from_currency_code == from_currency,
                ExchangeRate.to_currency_code == to_currency,
                ExchangeRate.rate_date <= rate_date
            )
        ).order_by(ExchangeRate.rate_date.desc()).first()
        
        return latest_rate.rate if latest_rate else None
    
    @staticmethod
    def convert_amount(
        db: Session,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        rate_date: Optional[date] = None
    ) -> Optional[Decimal]:
        """Convert amount from one currency to another"""
        rate = CurrencyService.get_exchange_rate(db, from_currency, to_currency, rate_date)
        if rate:
            return amount * rate
        return None
