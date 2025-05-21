
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_password_hash
from user.models import User
from user.schemas import UserCreate
from sqlalchemy.exc import IntegrityError


def create_user(db: Session, user_in: UserCreate):

    # Check if username already exists
    user_exists = db.query(User).filter(User.username == user_in.username).first()


    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    email_exists = db.query(User).filter(User.email_id == user_in.email_id).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if phone number already exists
    phone_exists = db.query(User).filter(User.phone_no == user_in.phone_no).first()
    if phone_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    if not user_in.first_name.strip() or not user_in.last_name.strip():
        raise HTTPException(
            status_code=422,
            detail="First name and last name cannot be empty"
        )
    
    # Create new user
    try:
        hashed_password = get_password_hash(user_in.password)
        user_in.password = hashed_password
        db_user = User(**user_in.model_dump(), is_profile_created=True)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed due to database constraint violation"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {str(e)}"
        )