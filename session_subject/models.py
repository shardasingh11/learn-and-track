from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from db.base_model import BaseModel
import enum



class LearningStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Subject(BaseModel):
    __tablename__ = "subjects"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_name = Column(String, unique=True, index=True, nullable=False)
    learning_status = Column(Enum(LearningStatus), default=LearningStatus.IN_PROGRESS)
    
    # Relationships with cascade - these are fine to define here
    user = relationship("User", back_populates="subjects")
    sessions = relationship("SubjectSession", back_populates="subject", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class SubjectSession(BaseModel):
    __tablename__ = "subject_sessions"

    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_time = Column(Integer, nullable=True)  # Stored in minutes
   
    # Basic relationships
    user = relationship("User", back_populates="sessions")
    subject = relationship("Subject", back_populates="sessions")
    
    # Many-to-many with Topic through TopicSession
    topic_sessions = relationship("TopicSession", back_populates="session", cascade="all, delete-orphan")


class Topic(BaseModel):
    __tablename__ = "topics"

    topic_name = Column(String, nullable=False)
    topic_description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    subject = relationship("Subject", back_populates="topics")
    # Many-to-many with SubjectSession through TopicSession
    topic_sessions = relationship("TopicSession", back_populates="topic", cascade="all, delete-orphan")

class TopicSession(BaseModel):
    __tablename__ = "topic_session"

    topic_id = Column(
        Integer, 
        ForeignKey("topics.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    session_id = Column(
        Integer, 
        ForeignKey("subject_sessions.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    

    # Relationships
    topic = relationship("Topic", back_populates="topic_sessions")
    session = relationship("SubjectSession", back_populates="topic_sessions")