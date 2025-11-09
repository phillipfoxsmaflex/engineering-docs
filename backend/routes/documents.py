

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
from models.folder import Folder as FolderModel

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)

class DocumentBase(BaseModel):
    title: str
    description: str | None = None
    document_number: str

class DocumentCreate(DocumentBase):
    folder_id: int | None = None

class DocumentUpdate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int
    creator_id: int
    folder_id: int | None
    created_at: datetime
    status: str

    class Config:
        orm_mode = True

@router.post("/", response_model=DocumentRead)
async def create_document(
    title: str = Form(...),
    description: str = Form(None),
    document_number: str = Form(...),
    folder_id: int = Form(None),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):
    # Validate folder exists if provided
    if folder_id:
        query = FolderModel.__table__.select().where(FolderModel.id == folder_id)
        folder = await database.fetch_one(query)
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

    # Create document record in DB
    query = DocumentModel.__table__.insert().values(
        title=title,
        description=description,
        document_number=document_number,
        creator_id=current_user.id,
        folder_id=folder_id,
        status="Entwurf"  # Default status is "Draft"
    )
    document_id = await database.execute(query)

    # Save file to disk
    file_location = f"uploads/documents/{document_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create document version record in DB
    query = DocumentVersionModel.__table__.insert().values(
        document_id=document_id,
        version_number="v1.0",
        file_path=file_location
    )
    await database.execute(query)

    return {
        "id": document_id,
        "title": title,
        "description": description,
        "document_number": document_number,
        "creator_id": current_user.id,
        "folder_id": folder_id,
        "created_at": datetime.utcnow(),
        "status": "Entwurf"
    }

@router.get("/", response_model=List[DocumentRead])
async def read_documents():
    query = DocumentModel.__table__.select()
    documents = await database.fetch_all(query)
    return documents

@router.get("/{document_id}", response_model=DocumentRead)
async def read_document(document_id: int):
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

@router.put("/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: int,
    title: str = Form(...),
    description: str = Form(None),
    document_number: str = Form(...),
    folder_id: int = Form(None),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Validate folder exists if provided
    if folder_id:
        query = FolderModel.__table__.select().where(FolderModel.id == folder_id)
        folder = await database.fetch_one(query)
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

    # Update document record in DB
    query = DocumentModel.__table__.update().where(DocumentModel.id == document_id).values(
        title=title,
        description=description,
        document_number=document_number,
        folder_id=folder_id
    )
    await database.execute(query)

    return {
        "id": document_id,
        "title": title,
        "description": description,
        "document_number": document_number,
        "creator_id": document.id,
        "folder_id": folder_id,
        "created_at": document.created_at,
        "status": document.status
    }

@router.delete("/{document_id}")
async def delete_document(document_id: int, current_user: UserModel = Depends(get_current_user)):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete document record from DB
    query = DocumentModel.__table__.delete().where(DocumentModel.id == document_id)
    await database.execute(query)

    # Delete files from disk
    file_path = f"uploads/documents/{document_id}"
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

    return {"detail": "Document deleted successfully"}

