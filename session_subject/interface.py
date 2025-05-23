from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from session_subject.models import LearningStatus, Subject, SubjectSession, Topic, TopicSession
from session_subject.schemas import CreateSessionRequest, SubjectCreate, SubjectStatusUpdate, TopicCreateOrGet
from user.models import User



def create_subjects(db: Session, subject: SubjectCreate, user_id: int):
     # Check if subject with the same name already exists
    db_subject = db.query(Subject).filter(Subject.subject_name == subject.subject_name).first()
    if db_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subject with name '{subject.subject_name}' already exists"
        )

    
    # Create new subject
    new_subject = Subject(**subject.model_dump(), user_id=user_id)
    
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
    
   
    subject.learning_status = status_update.learning_status  # type: ignore
    
    db.commit()
    db.refresh(subject)
    
    return subject



def get_or_create_topic(db: Session, topic_data: TopicCreateOrGet) -> Topic:
    """
    Retrieves an existing topic or creates a new one if it doesn't exist.
    
    Args:
        db: Database session
        topic_data: Pydantic model containing topic information
        
    Returns:
        Topic: Retrieved or newly created Topic object
    """
    # Check if topic exists
    topic = db.query(Topic).filter(
        Topic.topic_name == topic_data.name,
        Topic.subject_id == topic_data.subject_id
    ).first()
    
    # Create new topic if it doesn't exist
    if not topic:
        topic = Topic(
            topic_name=topic_data.name,
            topic_description=topic_data.description,
            subject_id=topic_data.subject_id
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)
        
    
    return topic

def create_session(db: Session, session_data: CreateSessionRequest, user_id: int):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for given user id {user_id}"
        )
     # Create a new session with all data at once

    db_subject = db.query(Subject).filter(Subject.id == session_data.subject_id).first()

    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")



    new_session = SubjectSession(
        subject_id=session_data.subject_id,
        user_id=user_id,
        start_time=session_data.start_time,
        end_time=session_data.end_time,
        total_time=session_data.total_time  # Frontend calculates this or backend calculates it
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    # Create or link topics
    topics = []
    for topic_item in session_data.topics:
        # Check if topic exists
        topic_data = TopicCreateOrGet(
            name=topic_item.name,
            description=topic_item.description,
            subject_id=session_data.subject_id
        )
         
        # Get or create the topic using the Pydantic model
        topic = get_or_create_topic(db=db, topic_data=topic_data)
    
        topics.append(topic)
        
        
        # Add to junction table
        topic_session_obj = TopicSession(topic_id=topic.id, session_id=new_session.id)
        db.add(topic_session_obj)
    
    
    # Return response with session details
    response = {
        "id": new_session.id,
        "subject": {"id": session_data.subject_id, "name": db_subject.subject_name},
        "start_time": new_session.start_time,
        "end_time": new_session.end_time,
        "total_time": new_session.total_time,
        "topics": [{"id": t.id, "name": t.topic_name, "description": t.topic_description} for t in topics]
    }
    
    return response