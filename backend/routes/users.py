



from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List

from database import database
from models.user import User as UserModel
from core.security import get_password_hash, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate):
    query = UserModel.__table__.insert().values(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True
    )
    user_id = await database.execute(query)

    return {**user.dict(), "id": user_id, "is_active": True}

@router.get("/", response_model=List[UserRead])
async def read_users():
    query = UserModel.__table__.select()
    users = await database.fetch_all(query)
    return users


