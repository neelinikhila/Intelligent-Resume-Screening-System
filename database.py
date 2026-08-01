from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Change the password below to the password you created during PostgreSQL installation
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:5007@localhost:5432/resume_screening"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()