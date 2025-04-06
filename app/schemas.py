from pydantic import BaseModel, Field
from typing import Annotated


class LoginValidation(BaseModel):
    username: Annotated[str, Field(max_length=15)]
    password: Annotated[str, Field(max_length=10)]


class RegisterValidation(LoginValidation):
    email: Annotated[str, Field(max_length=255)]


class Token(BaseModel):
    access_token: str
    token_type: str