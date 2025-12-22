from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.finance import CashTransaction, BankTransaction, CashTransactionType
from ..models.accounting import CashAccount, BankAccount
from ..services.sequence_service import SequenceService
from ..services.journal_service import JournalEngine
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/finance", tags=["finance"])

class CashTransactionCreate(BaseModel):
    cash_account_id: uuid.UUID
    transaction_type: CashTransactionType
    amount: float
    description: str
    partner_id: uuid.UUID = None

@router.post("/cash-transaction")
async def create_cash_transaction(tx_in: CashTransactionCreate, db: Session = Depends(get_db)):
    workspace_id = uuid.uuid4() # Mock
    ref_no = SequenceService.get_next_number(db, workspace_id, "CASH", "KAS")
    
    db_tx = CashTransaction(**tx_in.dict(), workspace_id=workspace_id, ref_no=ref_no)
    db.add(db_tx)
    db.commit()
    
    # Auto-journal: Debit/Credit Cash Account
    entries = []
    if tx_in.transaction_type == CashTransactionType.RECEIPT:
        entries.append({'coa_code': '1101', 'debit': tx_in.amount, 'credit': 0})  # Cash
        entries.append({'coa_code': '4101', 'debit': 0, 'credit': tx_in.amount})  # Revenue or other
    else:
        entries.append({'coa_code': '1101', 'debit': 0, 'credit': tx_in.amount})  # Cash
        entries.append({'coa_code': '5101', 'debit': tx_in.amount, 'credit': 0})  # Expense
    
    journal = JournalEngine.create_journal_entry(
        db, workspace_id, ref_no, tx_in.description, "CASH", db_tx.id, entries
    )
    db_tx.journal_id = journal.id
    db.commit()
    
    return {"message": "Cash transaction recorded", "ref": ref_no}

@router.get("/cash-accounts")
async def list_cash_accounts(db: Session = Depends(get_db)):
    return db.query(CashAccount).all()

@router.get("/bank-accounts")
async def list_bank_accounts(db: Session = Depends(get_db)):
    return db.query(BankAccount).all()
