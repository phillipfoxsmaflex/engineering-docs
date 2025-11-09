


from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import database
from models.document import Document as DocumentModel
from core.deps import get_current_user
from models.user import User as UserModel

router = APIRouter(
    prefix="/document-status",
    tags=["document_status"],
    responses={404: {"description": "Not found"}},
)

class DocumentStatusUpdate(BaseModel):
    status: str
    comment: str | None = None

class DocumentRead(BaseModel):
    id: int
    title: str
    description: str | None
    document_number: str
    creator_id: int
    folder_id: int | None
    created_at: datetime
    status: str

    model_config = {"from_attributes": True}

@router.put("/{document_id}", response_model=DocumentRead)
async def update_document_status(
    document_id: int,
    status_update: DocumentStatusUpdate = Depends(),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Validate status transition
    valid_status_transitions = {
        "Entwurf": ["In Prüfung"],
        "In Prüfung": ["Genehmigt", "Abgelehnt"],
        "Genehmigt": [],  # Final state
        "Abgelehnt": ["Entwurf"]  # Can go back to draft with feedback
    }

    if document.status not in valid_status_transitions or status_update.status not in valid_status_transitions[document.status]:
        raise HTTPException(status_code=400, detail="Invalid status transition")

    # Update document status
    query = DocumentModel.__table__.update().where(DocumentModel.id == document_id).values(
        status=status_update.status,
    )
    await database.execute(query)

    # Fetch the updated document
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    updated_document = await database.fetch_one(query)
    
    return updated_document

@router.get("/{document_id}", response_model=DocumentRead)
async def get_document_status(document_id: int):
    # Check if the document exists
    query = DocumentModel.__table__.select().where(DocumentModel.id == document_id)
    document = await database.fetch_one(query)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

