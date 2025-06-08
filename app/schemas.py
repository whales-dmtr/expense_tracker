from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, String
from sqlalchemy import Sequence


class UserData(BaseModel):
    id: None | int = None
    username: str
    email: EmailStr
    password: None | str


class ExpenseData(BaseModel):
    id: None | int = None
    description: str
    amount: float
    time_created: None | str = None
    category: None | str = None


class ExpenseDataModifid(ExpenseData):
    description: None | str = None
    amount: None | float = None


class Token(BaseModel):
    access_token: str
    token_type: str


users_id_seq = Sequence('users_id_seq')


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(default=users_id_seq.next_value(), primary_key=True)
    username: str = Field(String(50), unique=True, nullable=False)
    password: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)

    def convert_to_user_data(self) -> UserData:
        user_data = UserData(
            id=self.id,
            username=self.username,
            password=None,
            email=self.email
        )
        return user_data


expenses_id_seq = Sequence('expenses_id_seq')


class Expense(SQLModel, table=True):
    __tablename__ = 'expenses'

    id: Optional[int] = Field(
        default=expenses_id_seq.next_value(), primary_key=True)
    description: str = Field(min_length=1, max_length=50, nullable=False)
    amount: float = Field(gt=0, nullable=False)
    time_created: datetime = Field(nullable=False)
    category: str = Field(min_length=6, max_length=11)
    user_id: int = Field(foreign_key="users.id")
