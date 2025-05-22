from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from db.base_model import BaseModel
from sqlalchemy.orm import relationship
import enum
from session_subject.models import SubjectSession, Subject


class ProfileType(enum.Enum):
    STUDENT = "Student"
    DEVELOPER = "Developer"
    WRITER = "Writer"
    TEACHER = "Teacher"
    SOFTWARE_ENGINEER = "Software Engineer"
    ENGINEER = "Engineer"
    OTHER = "Other"

class UseType(enum.Enum):
    PERSONAL = "personal"
    WORK = "work"

class LearnerUserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email_id = Column(String, unique=True, index=True, nullable=False)
    profile_description = Column(Enum(ProfileType), nullable=False)
    use_type = Column(Enum(UseType), nullable=False)
    phone_no = Column(String(20), unique=True, nullable=False)
    password = Column(String, nullable=False)  # Should be hashed
    is_profile_created = Column(Boolean, default=False)
    user_role = Column(Enum(LearnerUserRole), nullable=False, default=LearnerUserRole.USER)
   
     # Relationships with cascade
    subjects = relationship("UserSubject", back_populates="user", cascade="all, delete-orphan")
    sub_sessions = relationship("SubjectSession", back_populates="user", cascade="all, delete-orphan")


class UserSubject(BaseModel):
    __tablename__ = "user_subjects"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
   
    
    # Relationships
    user = relationship("User", back_populates="subjects")
    subject = relationship("Subject", back_populates="users")