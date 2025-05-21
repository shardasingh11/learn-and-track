from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from session_subject.models import LearningStatus, Subject
from session_subject.schemas import SubjectCreate, SubjectStatusUpdate



def create_subjects(db: Session, subject: SubjectCreate):
     # Check if subject with the same name already exists
    db_subject = db.query(Subject).filter(Subject.subject_name == subject.subject_name).first()
    if db_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subject with name '{subject.subject_name}' already exists"
        )
    
    # Convert Pydantic enum to SQLAlchemy enum
    learning_status = LearningStatus[subject.learning_status.value.upper()]
    
    # Create new subject
    new_subject = Subject(
        subject_name=subject.subject_name,
        learning_status=learning_status
    )
    
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    
    return new_subject


# update subject's status
def update_subject_status_only(
    db: Session, 
    status_update: SubjectStatusUpdate, 
    subject_id: int
):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with ID {subject_id} not found"
        )
    
    # Update only the learning status
    learning_status = LearningStatus[status_update.learning_status.value.upper()]
    subject.learning_status = learning_status # type: ignore
    
    db.commit()
    db.refresh(subject)
    
    return subject

