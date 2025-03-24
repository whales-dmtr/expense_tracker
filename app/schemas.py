from pydantic import BaseModel, Field


class LoginValidation(BaseModel):
    username: str = Field(max_length=15)
    password: str = Field(max_length=10)


class RegisterValidation(LoginValidation):
    email: str = Field(max_length=255)
