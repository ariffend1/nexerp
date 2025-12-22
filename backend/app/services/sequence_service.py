import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.core.database import Base

class DocumentSequence(Base):
    __tablename__ = "document_sequences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    prefix = Column(String)
    module = Column(String) # e.g., 'PO', 'SO', 'SPK', 'GRN'
    last_number = Column(Integer, default=0)

class SequenceService:
    @staticmethod
    def get_next_number(db: Session, workspace_id: uuid.UUID, module: str, prefix: str):
        seq = db.query(DocumentSequence).filter(
            DocumentSequence.workspace_id == workspace_id,
            DocumentSequence.module == module
        ).first()

        if not seq:
            seq = DocumentSequence(workspace_id=workspace_id, module=module, prefix=prefix, last_number=0)
            db.add(seq)
            db.flush()
        
        seq.last_number += 1
        db.add(seq)
        db.commit()
        
        # Format: PREFIX-2025-0001
        import datetime
        year = datetime.datetime.now().year
        return f"{seq.prefix}-{year}-{str(seq.last_number).zfill(4)}"
