import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Enum as SqlEnum, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class PartnerCategory(str, enum.Enum):
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    BOTH = "both"

class COAType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"

class Partner(Base):
    __tablename__ = "partners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String)
    category = Column(SqlEnum(PartnerCategory))
    credit_limit = Column(Numeric(18, 2), default=0)
    address = Column(Text)

class COA(Base):
    __tablename__ = "chart_of_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    code = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(SqlEnum(COAType))
    parent_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"), nullable=True)
    is_active = Column(Boolean, default=True)

class CashAccount(Base):
    __tablename__ = "cash_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    coa_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"))
    name = Column(String)
    currency = Column(String, default="IDR")

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    coa_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"))
    bank_name = Column(String)
    account_number = Column(String)
    currency = Column(String, default="IDR")

class FixedAsset(Base):
    __tablename__ = "fixed_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    asset_code = Column(String, unique=True, index=True)
    name = Column(String)
    purchase_date = Column(DateTime)
    purchase_cost = Column(Numeric(18, 2))
    salvage_value = Column(Numeric(18, 2), default=0)
    useful_life_years = Column(Integer)
    accumulated_depreciation = Column(Numeric(18, 2), default=0)
    coa_asset_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"))
    coa_depreciation_id = Column(UUID(as_uuid=True), ForeignKey("chart_of_accounts.id"))
