from datetime import datetime

from sqlmodel import SQLModel, Field, String
from sqlalchemy import Sequence
from pydantic import EmailStr

from app.schemas import UserData


users_id_seq = Sequence('users_id_seq')
expenses_id_seq = Sequence('expenses_id_seq')


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


class Expense(SQLModel, table=True):
    __tablename__ = 'expenses'

    id: int = Field(
        default=expenses_id_seq.next_value(), primary_key=True)
    description: str = Field(min_length=1, max_length=50, nullable=False)
    amount: float = Field(gt=0, nullable=False)
    time_created: datetime = Field(nullable=False)
    category: str = Field(min_length=6, max_length=11, nullable=False)
    user_id: int = Field(foreign_key="users.id")
