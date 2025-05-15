from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Enable SQL query logging
    pool_size=3,  # 3 connections per worker → 4×3 = 12
    max_overflow=1,  # Up to 1 extra per worker if needed → max 4 more = 16
    pool_timeout=30,  # Wait time for a free connection
    pool_pre_ping=True,  # Ensures stale connections are reused
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    with SessionLocal() as db:
        yield db
