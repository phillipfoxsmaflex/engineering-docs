


import os
import shutil
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel
from typing import List

from database import database
from models.document import Document as DocumentModel, DocumentVersion as DocumentVersionModel
from core.deps import get_current_user
from models.user import User as UserModel

router = APIRouter(
    prefix="/document-versions",
    tags=["document_versions"],
    responses={404: {"description": "Not found"}},
)

class DocumentVersionBase(BaseModel):
    document_id: int
    version_number: str
    file_path: str
    comment: str | None = None

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersionUpdate(BaseModel):
    comment: str | None = None

class DocumentVersionRead(DocumentVersionBase):
    id: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}

@router.post("/", response_model=DocumentVersionRead)
async def create_document_version(
    document_id: int = Form(...),
    comment: str = Form(None),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Determine new version number
    query = DocumentVersionModel.__table__.select().where(DocumentVersionModel.document_id == document_id).order_by(DocumentVersionModel.uploaded_at.desc())
    last_version = await database.fetch_one(query)

    if last_version:
        # Extract the numeric part of the version, increment it
        parts = last_version.version_number[1:].split('.')
        major = int(parts[0])
        minor = int(parts[1]) + 1

        # Check if we need to increment the major version (every 10 minor versions)
        if minor >= 10:
            major += 1
            minor = 0

        new_version_number = f"v{major}.{minor}"
    else:
        new_version_number = "v1.0"

    # Save file to disk
    file_location = f"uploads/documents/{document_id}/versions/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create document version record in DB
    query = DocumentVersionModel.__table__.insert().values(
        document_id=document_id,
        version_number=new_version_number,
        file_path=file_location,
        comment=comment
    )
    version_id = await database.execute(query)

    return {
        "id": version_id,
        "document_id": document_id,
        "version_number": new_version_number,
        "file_path": file_location,
        "uploaded_at": datetime.utcnow(),
        "comment": comment
    }

@router.get("/", response_model=List[DocumentVersionRead])
async def read_document_versions():
    query = DocumentVersionModel.__table__.select()
    versions = await database.fetch_all(query)
    return versions

@router.get("/document/{document_id}", response_model=List[DocumentVersionRead])
async def read_document_versions_by_document(document_id: int):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    query = DocumentVersionModel.__table__.select().where(DocumentVersionModel.document_id == document_id)
    versions = await database.fetch_all(query)
    return versions

@router.put("/{version_id}", response_model=DocumentVersionRead)
async def update_document_version(
    version_id: int,
    comment: str = Form(None),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the version exists
    query = DocumentVersionModel.__table__.select().where(DocumentVersionModel.id == version_id)
    version = await database.fetch_one(query)

    if not version:
        raise HTTPException(status_code=404, detail="Document version not found")

    # Update document version record in DB
    query = DocumentVersionModel.__table__.update().where(DocumentVersionModel.id == version_id).values(
        comment=comment
    )
    await database.execute(query)

    return {
        "id": version_id,
        "document_id": version.document_id,
        "version_number": version.version_number,
        "file_path": version.file_path,
        "uploaded_at": version.uploaded_at,
        "comment": comment
    }

