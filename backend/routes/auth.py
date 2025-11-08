



from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from ..database import database
from ..models.user import User as UserModel
from ..core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from datetime import timedelta
import sqlalchemy

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class LoginForm(BaseModel):
    username: str
    password: str

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: LoginForm):
    query = UserModel.__table__.select().where(UserModel.email == form_data.username)
    user = await database.fetch_one(query)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin-init")
async def initialize_admin():
    """
    Initialize the admin account with username 'admin' and password 'password123'
    if no users exist in the database. This endpoint is intended for first-time setup.
    """
    # Check if any users exist
    query = sqlalchemy.select([sqlalchemy.func.count(UserModel.id)])
    user_count = await database.execute(query)

    if user_count == 0:
        # Create admin user with hardcoded credentials
        hashed_password = get_password_hash("password123")
        query = UserModel.__table__.insert().values(
            email="admin@example.com",
            hashed_password=hashed_password,
            is_admin=True
        )
        await database.execute(query)
        return {"message": "Admin user created successfully with username 'admin' and password 'password123'"}
    else:
        return {"message": f"{user_count} users already exist. Admin creation skipped."}

