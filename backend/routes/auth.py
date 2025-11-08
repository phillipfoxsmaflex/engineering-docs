



from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from ..database import database
from ..models.user import User as UserModel
from ..core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

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

