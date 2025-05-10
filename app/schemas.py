from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field


class UserLoginData(BaseModel):
    """
    This schema has made for control a length of username and password 
    when user is logging in.
    """
    username: str
    password: str


class UserFullData(UserLoginData):
    id: None | int
    """
    This schema has made for control a length of username, password and email 
    when user is registering.
    """
    email: str


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