"""Pytest configuration and fixtures"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base
from app.database.session import get_db


# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with overridden database"""

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Fixture with test user data"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "display_name": "Test User",
    }


@pytest.fixture
def test_bottle_data():
    """Fixture with test bottle data"""
    return {
        "name": "1792 Small Batch Bourbon",
        "spirit_type": "whiskey",
        "distillery": "Barton 1792 Distillery",
        "proof": 100,
        "region": "Kentucky",
        "country": "United States",
    }
