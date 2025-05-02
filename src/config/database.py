import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.environments import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


def get_db():
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as db:
        yield db
