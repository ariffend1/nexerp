from sqlalchemy.orm import Session
from app.models.journals import Journal, JournalItem
from app.models.accounting import COA
from uuid import UUID
from datetime import date

class JournalEngine:
    @staticmethod
    def create_journal_entry(
        db: Session,
        workspace_id: UUID,
        ref_no: str,
        description: str,
        source_type: str,
        source_id: UUID,
        entries: list # list of dicts: {'coa_code': '1101', 'debit': 100, 'credit': 0, 'partner_id': None}
    ):
        new_journal = Journal(
            workspace_id=workspace_id,
            date=date.today(),
            ref_no=ref_no,
            description=description,
            source_type=source_type,
            source_id=source_id,
            approval_status="pending"
        )
        db.add(new_journal)
        db.flush()

        for item in entries:
            coa = db.query(COA).filter(COA.code == item['coa_code'], COA.workspace_id == workspace_id).first()
            if not coa:
                continue # In production, throw error or create default COA
            
            ji = JournalItem(
                journal_id=new_journal.id,
                coa_id=coa.id,
                debit=item['debit'],
                credit=item['credit'],
                partner_id=item.get('partner_id')
            )
            db.add(ji)
        
        db.commit()
        return new_journal
