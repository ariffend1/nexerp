from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal
from datetime import date
from ..models.currency_tax import TaxRate, TaxTransaction, TaxType
import uuid

class TaxService:
    """Indonesian tax calculation service"""
    
    # PPh 21 progressive tax brackets (2024)
    PPH_21_BRACKETS = [
        (60000000, 0.05),    # Up to 60M: 5%
        (250000000, 0.15),   # 60M-250M: 15%
        (500000000, 0.25),   # 250M-500M: 25%
        (5000000000, 0.30),  # 500M-5B: 30%
        (float('inf'), 0.35) # Above 5B: 35%
    ]
    
    @staticmethod
    def seed_tax_rates(db: Session, workspace_id: uuid.UUID):
        """Seed Indonesian tax rates"""
        today = date.today()
        
        tax_configs = [
            {
                "tax_type": TaxType.PPN.value,
                "rate_percentage": Decimal("11.00"),
                "description": "PPN (VAT) 11% - Standard rate",
                "effective_from": date(2022, 4, 1)
            },
            {
                "tax_type": TaxType.PPH_23.value,
                "rate_percentage": Decimal("2.00"),
                "description": "PPh 23 - Withholding tax for services/rent",
                "effective_from": date(2020, 1, 1)
            },
            {
                "tax_type": TaxType.PPH_4_2.value,
                "rate_percentage": Decimal("10.00"),
                "description": "PPh 4(2) - Final tax for construction services",
                "effective_from": date(2020, 1, 1)
            },
        ]
        
        for tax_config in tax_configs:
            existing = db.query(TaxRate).filter(
                and_(
                    TaxRate.workspace_id == workspace_id,
                    TaxRate.tax_type == tax_config["tax_type"],
                    TaxRate.is_active == True
                )
            ).first()
            
            if not existing:
                tax_rate = TaxRate(workspace_id=workspace_id, **tax_config)
                db.add(tax_rate)
        
        db.commit()
    
    @staticmethod
    def calculate_ppn(amount: Decimal, include_tax: bool = False) -> dict:
        """Calculate PPN (VAT) 11%"""
        ppn_rate = Decimal("0.11")
        
        if include_tax:
            # Amount already includes PPN, extract it
            base = amount / (Decimal("1") + ppn_rate)
            ppn = amount - base
        else:
            # Amount excludes PPN, add it
            base = amount
            ppn = amount * ppn_rate
        
        return {
            "base_amount": base,
            "ppn_amount": ppn,
            "total_amount": base + ppn,
            "ppn_rate": ppn_rate * 100
        }
    
    @staticmethod
    def calculate_pph_21(annual_income: Decimal, has_npwp: bool = True) -> dict:
        """Calculate PPh 21 (Income Tax) - Progressive brackets"""
        
        # PTKP (Tax-free threshold) - Single with no dependents
        ptkp = Decimal("54000000")  # 54M IDR per year
        
        # Taxable income
        taxable_income = max(annual_income - ptkp, Decimal("0"))
        
        if taxable_income == 0:
            return {
                "annual_income": annual_income,
                "ptkp": ptkp,
                "taxable_income": Decimal("0"),
                "tax_amount": Decimal("0"),
                "effective_rate": Decimal("0")
            }
        
        # Calculate tax using progressive brackets
        tax = Decimal("0")
        remaining = taxable_income
        previous_bracket = Decimal("0")
        
        for bracket_limit, rate in TaxService.PPH_21_BRACKETS:
            bracket_amount = min(remaining, Decimal(str(bracket_limit)) - previous_bracket)
            if bracket_amount <= 0:
                break
            
            tax += bracket_amount * Decimal(str(rate))
            remaining -= bracket_amount
            previous_bracket = Decimal(str(bracket_limit))
            
            if remaining <= 0:
                break
        
        # Non-NPWP penalty: 20% higher
        if not has_npwp:
            tax *= Decimal("1.20")
        
        return {
            "annual_income": annual_income,
            "ptkp": ptkp,
            "taxable_income": taxable_income,
            "tax_amount": tax,
            "effective_rate": (tax / annual_income * 100) if annual_income > 0 else Decimal("0"),
            "has_npwp": has_npwp
        }
    
    @staticmethod
    def calculate_pph_23(amount: Decimal, has_npwp: bool = True) -> dict:
        """Calculate PPh 23 (Withholding Tax) 2%"""
        rate = Decimal("0.02")
        
        # Non-NPWP: double rate (4%)
        if not has_npwp:
            rate = Decimal("0.04")
        
        tax_amount = amount * rate
        net_amount = amount - tax_amount
        
        return {
            "gross_amount": amount,
            "tax_rate": rate * 100,
            "tax_amount": tax_amount,
            "net_amount": net_amount,
            "has_npwp": has_npwp
        }
    
    @staticmethod
    def calculate_pph_4_2(amount: Decimal, service_type: str = "construction") -> dict:
        """Calculate PPh 4(2) (Final Tax)"""
        # Different rates for different services
        rates = {
            "construction": Decimal("0.025"),  # 2.5% for construction < 10M
            "rent": Decimal("0.10"),           # 10% for rent
            "other": Decimal("0.10")
        }
        
        rate = rates.get(service_type, Decimal("0.10"))
        tax_amount = amount * rate
        net_amount = amount - tax_amount
        
        return {
            "gross_amount": amount,
            "service_type": service_type,
            "tax_rate": rate * 100,
            "tax_amount": tax_amount,
            "net_amount": net_amount
        }
    
    @staticmethod
    def create_tax_transaction(
        db: Session,
        workspace_id: uuid.UUID,
        document_type: str,
        document_id: uuid.UUID,
        tax_type: str,
        tax_base: Decimal,
        tax_rate: Decimal,
        tax_amount: Decimal,
        npwp: str = None
    ) -> TaxTransaction:
        """Record tax transaction"""
        tax_transaction = TaxTransaction(
            workspace_id=workspace_id,
            document_type=document_type,
            document_id=document_id,
            tax_type=tax_type,
            tax_base=tax_base,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            npwp=npwp,
            tax_date=date.today()
        )
        db.add(tax_transaction)
        db.commit()
        db.refresh(tax_transaction)
        return tax_transaction
