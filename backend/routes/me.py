




from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.deps import get_current_user
from models.user import User as UserModel

router = APIRouter(
    prefix="/me",
    tags=["me"],
    responses={404: {"description": "Not found"}},
)

class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool

    model_config = {"from_attributes": True}

@router.get("/", response_model=UserRead)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user



