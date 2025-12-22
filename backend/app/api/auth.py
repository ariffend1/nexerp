from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.auth import User, Workspace
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    workspace_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", response_model=Token)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create Workspace
    new_workspace = Workspace(name=user_in.workspace_name)
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    
    # Create User
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        workspace_id=new_workspace.id,
        is_admin=True
    )
    db.add(new_user)
    db.commit()
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
