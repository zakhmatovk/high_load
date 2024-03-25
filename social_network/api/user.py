
from fastapi import APIRouter
from social_network.models.user import User

router = APIRouter()

@router.get("/user/get/{id}")
async def get_user(id: int) -> User:
    return await User.load(id)