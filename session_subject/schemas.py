from typing import Optional
from pydantic import BaseModel, Field

from session_subject.models import LearningStatus




class SubjectCreate(BaseModel):
    subject_name: str = Field(..., min_length=1, max_length=100)
    learning_status: LearningStatus = LearningStatus.NOT_STARTED

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