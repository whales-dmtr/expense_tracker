from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas import UserData
from app.routers.authentication import verify_token

router = APIRouter()


@router.get('/me', tags=['User'], summary="Get your username")
def get_username(user: Annotated[UserData, Depends(verify_token)]) -> dict[str, str]:
    return {'your_username': user.username}
