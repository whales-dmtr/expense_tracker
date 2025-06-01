from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserLoginData(BaseModel):
    """
    This schema has made for control a length of username and password 
    when user is logging in.
    """
    username: Annotated[str, Field(min_length=3, max_length=15)]
    password: Annotated[str, Field(min_length=4, max_length=20)]


class UserRegisterData(BaseModel):
    """
    This schema has made for control a length of username, password and email 
    when user is registering.
    """
    email: EmailStr
    password: str



class UserFullData(UserLoginData):
    """
    This schema has made for control a length of username, password and email 
    when user is registering.
    """
    id: int
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ExpenseData(BaseModel):
    desc: Annotated[str, Field(min_length=1, max_length=50)]
    amount: Annotated[float, Field(gt=0)]
    time_created: None | datetime = None
    category: None | Annotated[str, Field(min_length=6, max_length=11)] = None


class ExpenseFullData(ExpenseData):
    """
    All expense fields from db for full view.
    """
    expense_id: int
    owner: str
    time_created: str


