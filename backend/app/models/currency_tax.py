import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from decimal import Decimal
from app.core.database import Base

class Currency(Base):
    """Master data for supported currencies"""
    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(3), unique=True, index=True)  # ISO 4217: USD, EUR, IDR
    name = Column(String)
    symbol = Column(String(10))
    decimal_places = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ExchangeRate(Base):
    """Daily exchange rates"""
    __tablename__ = "exchange_rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_currency_code = Column(String(3), ForeignKey("currencies.code"))
    to_currency_code = Column(String(3), ForeignKey("currencies.code"))
    rate = Column(Numeric(20, 10))
    rate_date = Column(Date, index=True)
    source = Column(String)  # 'manual', 'api_fixer', 'api_exchangerate'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaxType(str, enum.Enum):
    """Indonesian tax types"""
    PPN = "ppn"  # VAT 11%
    PPH_21 = "pph_21"  # Income tax (progressive)
    PPH_23 = "pph_23"  # Withholding tax 2%
    PPH_4_2 = "pph_4_2"  # Final tax (rent, services)
    PPH_22 = "pph_22"  # Import tax
    PPH_25 = "pph_25"  # Installment income tax

class TaxRate(Base):
    """Tax rate configuration"""
    __tablename__ = "tax_rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    tax_type = Column(String)  # TaxType enum
    rate_percentage = Column(Numeric(5, 2))  # e.g., 11.00 for PPN
    description = Column(String)
    effective_from = Column(Date)
    effective_to = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaxTransaction(Base):
    """Tax calculations for transactions"""
    __tablename__ = "tax_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    document_type = Column(String)  # 'SO', 'PO', 'INVOICE', 'PAYROLL'
    document_id = Column(UUID(as_uuid=True))
    tax_type = Column(String)  # TaxType enum
    tax_base = Column(Numeric(20, 2))  # Amount subject to tax
    tax_rate = Column(Numeric(5, 2))
    tax_amount = Column(Numeric(20, 2))
    npwp = Column(String(20), nullable=True)  # Taxpayer ID
    tax_date = Column(Date)
    is_posted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
