from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.auth import User
from datetime import datetime
import uuid

security = HTTPBearer()

SECRET_KEY = "your-super-secret-key-for-development"  # Should be in .env
ALGORITHM = "HS256"

class AuthUser:
    """Current authenticated user context"""
    def __init__(self, user_id: uuid.UUID, workspace_id: uuid.UUID, email: str):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.email = email

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AuthUser:
    """
    Dependency to get current authenticated user from JWT token.
    Use this in route dependencies: user: AuthUser = Depends(get_current_user)
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        workspace_id: str = payload.get("workspace_id")
        email: str = payload.get("email")
        
        if user_id is None or workspace_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user exists and is active
        user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )
        
        return AuthUser(
            user_id=uuid.UUID(user_id),
            workspace_id=uuid.UUID(workspace_id),
            email=email
        )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """Additional check for active user (can be extended for premium features)"""
    return current_user
