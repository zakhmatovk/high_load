from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from common.model import RowNotFoundException
from social_network.models.user import User

router = APIRouter()


@router.get("/user/get/{id}")
async def get_user(id: str) -> User:
    user = await User.load(id)
    return user

class LoginRequest(BaseModel):
    id: str
    password: str

class LoginResponse(BaseModel):
    token: str

@router.post("/user/login")
async def login_user(r: LoginRequest) -> LoginResponse:
    try: 
        user = await User.load(r.id)
    except RowNotFoundException:
        raise HTTPException(status_code=403)
    if user.check_password(r.password):
        return LoginResponse(token=user.token())
    raise HTTPException(status_code=403)
