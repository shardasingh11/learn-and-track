from fastapi import FastAPI
from user.api import router as user_router
from session_subject.api import router as session_subject_router
from db.base_class import Base



app = FastAPI(title="Learn&track")

app.include_router(user_router)
app.include_router(session_subject_router)