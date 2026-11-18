"""
Pytest configuration and fixtures for Doctor Data Platform tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.utils.security import hash_password

# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_doctor_platform.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before tests, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fresh DB session per test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client():
    """Test client with DB override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def demo_user_token(client):
    """Register a demo user and return their token."""
    client.post("/api/auth/register", json={
        "email": "testuser@example.com",
        "password": "Test@1234",
        "full_name": "Test User",
    })
    response = client.post("/api/auth/login", data={
        "username": "testuser@example.com",
        "password": "Test@1234",
    })
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(demo_user_token):
    return {"Authorization": f"Bearer {demo_user_token}"}
