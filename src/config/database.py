from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

# ✅ Make sure the URL uses asyncpg driver
# e.g. postgresql+asyncpg://user:pass@host/db
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=3,
    max_overflow=1,
    pool_timeout=30,
    pool_pre_ping=True,
)

# Base for your models
Base = declarative_base()

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
