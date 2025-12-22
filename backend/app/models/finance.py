import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class CashTransactionType(str, enum.Enum):
    RECEIPT = "receipt"
    PAYMENT = "payment"

class CashTransaction(Base):
    __tablename__ = "cash_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    cash_account_id = Column(UUID(as_uuid=True), ForeignKey("cash_accounts.id"))
    ref_no = Column(String, unique=True, index=True)
    transaction_type = Column(SqlEnum(CashTransactionType))
    amount = Column(Numeric(18, 2))
    description = Column(String)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True)
    transaction_date = Column(DateTime, server_default=func.now())
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journals.id"), nullable=True)

class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.id"))
    ref_no = Column(String, unique=True, index=True)
    transaction_type = Column(SqlEnum(CashTransactionType))
    amount = Column(Numeric(18, 2))
    description = Column(String)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True)
    transaction_date = Column(DateTime, server_default=func.now())
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journals.id"), nullable=True)
