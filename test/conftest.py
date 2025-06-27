"""
Test configuration and fixtures for auth API testing.
Provides database setup, test client, and test user fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.config.database import Base, get_db
from src.main import app
from src.models.user_model import User
from src.utils.password_helper import get_password_hash
from src.config.constant import UserRole


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "bio": "Test user bio",
        "role": "user"
    }


@pytest.fixture
def test_admin_data():
    """Sample admin user data for testing."""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "AdminPass123!",
        "confirm_password": "AdminPass123!",
        "first_name": "Admin",
        "last_name": "User",
        "bio": "Admin user bio",
        "role": "admin"
    }


@pytest.fixture
def create_test_user(db_session):
    """Create a test user in the database."""
    def _create_user(username="testuser", email="testuser@example.com", password="TestPass123!", role=UserRole.user):
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hash_password=hashed_password,
            first_name="Test",
            last_name="User",
            role=role
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    return _create_user


@pytest.fixture
def valid_login_data():
    """Valid login credentials."""
    return {
        "username": "testuser",
        "password": "TestPass123!"
    }


@pytest.fixture
def invalid_login_data():
    """Invalid login credentials."""
    return {
        "username": "wronguser",
        "password": "wrongpass"
    }
