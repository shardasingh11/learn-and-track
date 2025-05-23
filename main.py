from fastapi import FastAPI
from db.base_class import Base

from user.api import router as user_router
from session_subject.api import router as session_subject_router
from auth.api import router as auth_router





app = FastAPI(title="Learn&track")


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(session_subject_router)