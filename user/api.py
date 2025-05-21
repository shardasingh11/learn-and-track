from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Any
from .interface import create_user

from user.schemas import UserCreate, UserResponse
from user.models import User
from core.security import get_password_hash
from db.session import get_db

router = APIRouter(prefix="/users", tags=["user"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    
    return create_user(db=db, user_in=user_in)
  
   