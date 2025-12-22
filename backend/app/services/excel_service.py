import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from typing import List, Dict
import uuid

class ExcelService:
    @staticmethod
    def export_to_excel(data: List[Dict], filename: str = "export.xlsx") -> BytesIO:
        """Export list of dictionaries to Excel"""
        df = pd.DataFrame(data)
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        output.seek(0)
        return output
    
    @staticmethod
    def import_from_excel(file: BytesIO, model_class, db: Session, workspace_id: uuid.UUID):
        """Import Excel file to database model"""
        df = pd.read_excel(file)
        
        records_created = 0
        for _, row in df.iterrows():
            record_data = row.to_dict()
            record_data['workspace_id'] = workspace_id
            
            # Create instance of model
            db_record = model_class(**record_data)
            db.add(db_record)
            records_created += 1
        
        db.commit()
        return {"message": f"{records_created} records imported successfully"}
    
    @staticmethod
    def get_template(model_fields: List[str]) -> BytesIO:
        """Generate Excel template with column headers"""
        df = pd.DataFrame(columns=model_fields)
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Template')
        
        output.seek(0)
        return output
