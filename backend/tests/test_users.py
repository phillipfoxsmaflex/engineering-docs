
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from databases import Database

from main import app
from database import database, Base
from models.user import User as UserModel

# Create a new database for testing
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
async def db():
    # Create the database tables
    engine = create_engine(DATABASE_URL)
    async with database:
        await database.connect()
        await database.execute(Base.metadata.create_all(engine))

    yield database

    # Drop the database tables after testing
    async with database:
        await database.disconnect()
        await database.execute(Base.metadata.drop_all(engine))

@pytest.mark.asyncio
async def test_create_user(test_client, db):
    response = test_client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True

@pytest.mark.asyncio
async def test_read_users(test_client, db):
    # First create a user
    await db.execute(
        UserModel.__table__.insert().values(
            email="testuser2@example.com",
            hashed_password="fakehashedpassword",
            is_active=True,
            is_admin=False
        )
    )

    response = test_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "email" in data[0]
