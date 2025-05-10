from typing import Annotated

from fastapi import FastAPI, Depends

import app.authentication as auth

from app.authentication import oauth2_scheme, get_username_by_id, verify_token


app = FastAPI()

app.include_router(auth.router)


@app.get('/me')
def get_username(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    user_id = verify_token(token)
    username = get_username_by_id(user_id)

    return {'your_username': username}