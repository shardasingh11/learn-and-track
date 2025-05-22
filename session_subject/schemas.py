from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from session_subject.models import LearningStatus




class SubjectCreate(BaseModel):
    subject_name: str = Field(..., min_length=1, max_length=100)
    learning_status: LearningStatus = LearningStatus.IN_PROGRESS

    class Config:
        schema_extra = {
            "example": {
                "subject_name": "Mathematics",
                "learning_status": "not_started"
            }
        }

class SubjectResponse(BaseModel):
    id: int
    subject_name: str
    learning_status: LearningStatus

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "subject_name": "Mathematics",
                "learning_status": "not_started"
            }
        }


class SubjectStatusUpdate(BaseModel):
    learning_status: LearningStatus

    class Config:
        schema_extra = {
            "example": {
                "learning_status": "in_progress"
            }
        }



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
    
    class Config:
        schema_extra = {
            "example": {
                "subject_id": 1,
                "user_id": 1,
                "start_time": "2025-05-21T10:00:00Z",
                "end_time": "2025-05-21T11:30:00Z",
                "total_time": 90,
                "topics": [
                    {
                        "name": "API Design",
                        "description": "Covered RESTful API design principles"
                    },
                    {
                        "name": "Pydantic Schemas",
                        "description": "Learned how to create request/response models"
                    }
                ]
            }
        }

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
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "subject": {"id": 1, "name": "Python Programming"},
                "start_time": "2025-05-21T10:00:00Z",
                "end_time": "2025-05-21T11:30:00Z",
                "total_time": 90,
                "topics": [
                    {
                        "id": 1,
                        "name": "API Design",
                        "description": "Covered RESTful API design principles"
                    },
                    {
                        "id": 2,
                        "name": "Pydantic Schemas",
                        "description": "Learned how to create request/response models"
                    }
                ]
            }
        }