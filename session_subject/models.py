from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from db.base_model import BaseModel
from user.models import User
import enum



class LearningStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Subject(BaseModel):
    __tablename__ = "subjects"

    subject_name = Column(String, unique=True, index=True, nullable=False)
    learning_status = Column(Enum(LearningStatus), default=LearningStatus.NOT_STARTED)
    
    # Relationships with cascade
    users = relationship("UserSubject", back_populates="subject", cascade="all, delete-orphan")
    sub_sessions = relationship("SubjectSession", back_populates="subject", cascade="all, delete-orphan")


class SubjectSession(BaseModel):
    __tablename__ = "subject_sessions"

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_name = Column(String, nullable=False)
    key_concept_name = Column(String, nullable=False)
    session_notes = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_time = Column(Integer, nullable=True)  # Stored in minutes
   
    
    # Relationships
    user = relationship("User", back_populates="sub_sessions")
    subject = relationship("Subject", back_populates="sub_sessions")