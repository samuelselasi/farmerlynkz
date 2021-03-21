from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import orm


class User(BaseModel):
    username: Optional[str] = Field(
        None, title="Full Name Optional Args"
    )
    email: Optional[EmailStr] = Field(
        None, title="Email Optional Args"
    )
    password: str = Field(
        None, title="Password Optional Args"
    )
    confirmPassword: str = Field(
        None, title="Confirm Password Optional Args"
    )


class LoginUser(User):
    email: EmailStr
    password: str = Field(min_length=12, max_length=100)


class SignupUser(LoginUser):
    username: str = Field(min_length=8, max_length=100)
    confirmPassword: str = Field(min_length=12, max_length=100)


class UserInDb(LoginUser):
    username: str = Field(min_length=8, max_length=100)

    class Config:
        orm_mode = True
