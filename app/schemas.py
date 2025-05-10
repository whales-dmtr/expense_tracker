from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone

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
    desc: Annotated[str, Field(min_length=1, max_length=50)]
    amount: Annotated[float, Field(gt=0)]
    time_created: Annotated[
        Optional[datetime],   
        # The default value of the field is the time of expense creation 
        Field(default_factory=datetime.now(timezone(timedelta(hours=3))))
    ]