from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, status

import app.authentication as auth
from app.authentication import oauth2_scheme, get_username_by_id
from app.constants import SECRET_KEY, ALGORITHM


app = FastAPI()

app.include_router(auth.router)


@app.get('/me')
def get_username(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    unauth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Your jwt is invalid.",
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        username = get_username_by_id(id)
        if id is None:
            raise unauth_error
        elif not username:
            raise unauth_error
        
        return {'your_username': username}
    except jwt.InvalidTokenError:
        raise unauth_error