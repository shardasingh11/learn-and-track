from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Database URL - change according to your database
DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()