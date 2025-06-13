from pydantic import BaseModel, EmailStr


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


class ExpenseDataModified(ExpenseData):
    description: None | str = None
    amount: None | float = None


class Token(BaseModel):
    access_token: str
    token_type: str
