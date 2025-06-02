from typing import Annotated

from fastapi import FastAPI, Depends

import app.authentication as auth
import app.expenses as expenses
from app.authentication import verify_token
from app.schemas import UserData


app = FastAPI()

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get('/me')
def get_username(user: Annotated[UserData, Depends(verify_token)]) -> dict[str, str]:
    return {'your_username': user.username}