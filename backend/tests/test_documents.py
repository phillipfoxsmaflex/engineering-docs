

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from databases import Database

from main import app
from database import database, Base
from models.user import User as UserModel
from models.document import Document as DocumentModel

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

@pytest.fixture(scope="module")
async def test_user(db):
    # Create a test user
    query = UserModel.__table__.insert().values(
        email="testuser@example.com",
        hashed_password="fakehashedpassword",
        is_active=True,
        is_admin=False
    )
    user_id = await db.execute(query)
    return {"id": user_id, "email": "testuser@example.com"}

@pytest.mark.asyncio
async def test_create_document(test_client, db, test_user):
    # Create a test folder first
    query = UserModel.__table__.insert().values(
        email="testuser2@example.com",
        hashed_password="fakehashedpassword",
        is_active=True,
        is_admin=False
    )
    user_id = await db.execute(query)

    files = {'file': ('test_file.txt', b'This is a test file content', 'text/plain')}
    form_data = {
        'title': 'Test Document',
        'description': 'A test document for testing',
        'document_number': 'DOC-12345',
        'folder_id': None
    }

    response = test_client.post("/documents/", data=form_data, files=files)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Document"
    assert data["document_number"] == "DOC-12345"

@pytest.mark.asyncio
async def test_read_documents(test_client, db):
    # First create a document
    query = DocumentModel.__table__.insert().values(
        title="Sample Document",
        description="A sample document for testing",
        document_number="SAMP-001",
        creator_id=1,
        status="Entwurf"
    )
    await db.execute(query)

    response = test_client.get("/documents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]

@pytest.mark.asyncio
async def test_read_document(test_client, db):
    # First create a document
    query = DocumentModel.__table__.insert().values(
        title="Sample Document",
        description="A sample document for testing",
        document_number="SAMP-002",
        creator_id=1,
        status="Entwurf"
    )
    document_id = await db.execute(query)

    response = test_client.get(f"/documents/{document_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sample Document"
    assert data["document_number"] == "SAMP-002"

