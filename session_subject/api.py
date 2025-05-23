from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from core.permissions import role_required
from db.session import get_db
from session_subject.models import LearningStatus, Subject
from session_subject.schemas import CreateSessionRequest, CreateSessionResponse, SubjectCreate, SubjectResponse, SubjectStatusUpdate
from user.models import LearnerUserRole
from user.schemas import UserDB
from .interface import create_session, create_subjects, update_subject_status_only

router = APIRouter(prefix="/session-subject",tags=["session's-subject"])



@router.post("/create-subject", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [LearnerUserRole.USER]
    ))
):
    
    return create_subjects(db=db, subject=subject, user_id=current_user.id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def update_subject_status(
    subject_id: int,
    status_update: SubjectStatusUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [LearnerUserRole.USER]
    ))

):
    
    return update_subject_status_only(db=db, status_update=status_update, subject_id=subject_id)



@router.post("/create-sessions/", response_model=CreateSessionResponse)
def create_subject_session(
    session_data: CreateSessionRequest, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(role_required(
        allowed_user_roles = [LearnerUserRole.USER]
    ))
):

    return create_session(db=db, session_data=session_data, user_id=current_user.id)
   