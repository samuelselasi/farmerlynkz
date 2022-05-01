from xmlrpc.client import DateTime
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
from sqlalchemy import DateTime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: Optional[str]
    user_type_id: int
    status: Optional[bool]
    firstname: str
    lastname: str
    othernames: Optional[str]
    phone: int
    dateofbirth: datetime.datetime


class UserUpdate(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]


class ResetPassword(BaseModel):
    password: str
    code: Optional[str]


class ChangePassword(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    user_type_id: int
    status: Optional[bool]
    firstname: str
    lastname: str
    othernames: Optional[str]
    phone: int
    dateofbirth: datetime.datetime

    class Config:
        orm_mode = True
