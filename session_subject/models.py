from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum, Table
from sqlalchemy.orm import relationship
from db.base_model import BaseModel
import enum



class LearningStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Subject(BaseModel):
    __tablename__ = "subjects"

    subject_name = Column(String, unique=True, index=True, nullable=False)
    learning_status = Column(Enum(LearningStatus), default=LearningStatus.IN_PROGRESS)
    
    # Relationships with cascade - these are fine to define here
    users = relationship("UserSubject", back_populates="subject", cascade="all, delete-orphan")
    sub_sessions = relationship("SubjectSession", back_populates="subject", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class SubjectSession(BaseModel):
    __tablename__ = "subject_sessions"

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_time = Column(Integer, nullable=True)  # Stored in minutes
   
    # Basic relationships
    user = relationship("User", back_populates="sub_sessions")
    subject = relationship("Subject", back_populates="sub_sessions")
    # The topics relationship will be defined later


class Topic(BaseModel):
    __tablename__ = "topics"

    topic_name = Column(String, nullable=False)
    topic_description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Basic relationship with Subject
    subject = relationship("Subject", back_populates="topics")
    # The sessions relationship will be defined later


# Junction table - define AFTER all the models it references
topic_session = Table(
    "topic_session",
    BaseModel.metadata,
    Column("topic_id", Integer, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
    Column("session_id", Integer, ForeignKey("subject_sessions.id", ondelete="CASCADE"), primary_key=True)
)

# Now define the many-to-many relationships that use the junction table
Topic.sessions = relationship("SubjectSession", secondary=topic_session, back_populates="topics")
SubjectSession.topics = relationship("Topic", secondary=topic_session, back_populates="sessions")