from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Any

from core.permissions import role_required
from .interface import create_user

from user.schemas import UserCreate, UserDB, UserResponse
from user.models import LearnerUserRole, User
from core.security import get_password_hash
from db.session import get_db

router = APIRouter(prefix="/users", tags=["user"])

@router.post("/register", response_model=UserResponse)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    if user_in.user_role == LearnerUserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin creation is not allowed from the frontend"
        )
    
    return create_user(db=db, user_in=user_in)

@router.get("/user", response_model=UserResponse)
async def get_user(
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [LearnerUserRole.USER, LearnerUserRole.ADMIN]
    ))
):
    return current_user
  
   