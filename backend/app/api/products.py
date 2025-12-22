from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.dependencies import get_current_user, AuthUser
from ..models.inventory import Product, ProductType, ValuationMethod
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/products", tags=["products"])

class ProductBase(BaseModel):
    code: str
    name: str
    uom: str
    type: ProductType
    valuation_method: ValuationMethod = ValuationMethod.AVERAGE
    base_price: float = 0

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: uuid.UUID
    workspace_id: uuid.UUID

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductOut])
async def list_products(db: Session = Depends(get_db), user: AuthUser = Depends(get_current_user)):
    products = db.query(Product).filter(Product.workspace_id == user.workspace_id).all()
    return products

@router.post("/", response_model=ProductOut])
async def create_product(product_in: ProductCreate, db: Session = Depends(get_db), user: AuthUser = Depends(get_current_user)):
    db_product = Product(**product_in.dict(), workspace_id=user.workspace_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
