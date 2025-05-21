from fastapi import FastAPI
from user.api import router as user_router
from db.base_class import Base



app = FastAPI(title="Learn&track")

app.include_router(user_router)