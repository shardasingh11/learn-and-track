from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from session_subject.models import LearningStatus




class SubjectCreate(BaseModel):
    user_id: int
    subject_name: str = Field(..., min_length=1, max_length=100)
    learning_status: LearningStatus = LearningStatus.IN_PROGRESS


class SubjectResponse(BaseModel):
    id: int
    user_id: int
    subject_name: str
    learning_status: LearningStatus


class SubjectStatusUpdate(BaseModel):
    learning_status: LearningStatus

class TopicCreateOrGet(BaseModel):
    """Pydantic model for getting or creating a topic"""
    name: str 
    description: Optional[str] 
    subject_id: int 

# Schema for topic data in request
class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Main request schema
class CreateSessionRequest(BaseModel):
    subject_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    total_time: int  # Stored in minutes
    topics: List[TopicCreate]
    
 
# Response schemas
class SubjectResponseForSession(BaseModel):
    id: int
    name: str

class TopicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class CreateSessionResponse(BaseModel):
    id: int
    subject: SubjectResponseForSession
    start_time: datetime
    end_time: datetime
    total_time: int
    topics: List[TopicResponse]
    
    