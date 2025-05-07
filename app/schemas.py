from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class LoginValidation(BaseModel):
    username: Annotated[str, Field(max_length=15)]
    password: Annotated[str, Field(max_length=10)]


class RegisterValidation(LoginValidation):
    email: Annotated[str, Field(max_length=255)]


class Token(BaseModel):
    access_token: str
    token_type: str


class ExpenseData(BaseModel):
    id: Optional[int]
    desc: Annotated[str, Field(max_length=50)]
    amount: float
    time_created: Optional[datetime]