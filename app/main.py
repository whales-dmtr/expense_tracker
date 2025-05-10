from typing import Annotated

from fastapi import FastAPI, Depends

import app.authentication as auth

from app.authentication import verify_token
from app.schemas import UserFullData


app = FastAPI()

app.include_router(auth.router)


@app.get('/me')
def get_username(user: Annotated[UserFullData, Depends(verify_token)]) -> dict[str, str]:
    return {'your_username': user.email}