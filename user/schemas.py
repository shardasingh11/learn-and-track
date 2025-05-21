from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from enum import Enum
from datetime import datetime

from user.models import ProfileType, UseType


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: int = Field(..., ge=0)
    email_id: EmailStr
    profile_description: ProfileType
    use_type: UseType
    phone_no: str = Field(..., max_length=20)
    password: str
    


class UserResponse(UserCreate):
    id: int
    is_profile_created: bool
  

    class Config:
        orm_mode = True