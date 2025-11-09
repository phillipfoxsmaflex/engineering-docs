
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from database import database
from models.folder import Folder as FolderModel
from core.deps import get_current_user
from models.user import User as UserModel

router = APIRouter(
    prefix="/folders",
    tags=["folders"],
    responses={404: {"description": "Not found"}},
)

class FolderBase(BaseModel):
    name: str

class FolderCreate(FolderBase):
    parent_id: int | None = None

class FolderUpdate(FolderBase):
    pass

class FolderRead(FolderBase):
    id: int

    model_config = {"from_attributes": True}

@router.post("/", response_model=FolderRead)
async def create_folder(folder: FolderCreate, current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    query = FolderModel.__table__.insert().values(
        name=folder.name,
        parent_id=folder.parent_id
    )
    folder_id = await database.execute(query)

    return {**folder.dict(), "id": folder_id}

@router.get("/", response_model=List[FolderRead])
async def read_folders():
    query = FolderModel.__table__.select().where(FolderModel.parent_id == None)
    folders = await database.fetch_all(query)
    return folders

@router.get("/{folder_id}", response_model=FolderRead)
async def read_folder(folder_id: int):
    query = FolderModel.__table__.select().where(FolderModel.id == folder_id)
    folder = await database.fetch_one(query)

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    return folder

@router.get("/{folder_id}/children", response_model=List[FolderRead])
async def read_folder_children(folder_id: int):
    query = FolderModel.__table__.select().where(FolderModel.parent_id == folder_id)
    folders = await database.fetch_all(query)
    return folders

@router.put("/{folder_id}", response_model=FolderRead)
async def update_folder(folder_id: int, folder: FolderUpdate, current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    query = FolderModel.__table__.update().where(FolderModel.id == folder_id).values(
        name=folder.name
    )
    await database.execute(query)

    return {**folder.dict(), "id": folder_id}

@router.delete("/{folder_id}")
async def delete_folder(folder_id: int, current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Check if the folder exists
    query = FolderModel.__table__.select().where(FolderModel.id == folder_id)
    folder = await database.fetch_one(query)

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    # Delete the folder
    query = FolderModel.__table__.delete().where(FolderModel.id == folder_id)
    await database.execute(query)

    return {"detail": "Folder deleted successfully"}
