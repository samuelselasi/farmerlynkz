from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


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


class BaseException(Exception):
    def __init__(self, message: str = None):
        self.message = message

    def _message(self):
        return self.message


class NotFoundError(BaseException):
    pass


class UnAcceptableError(BaseException):
    pass


class UnAuthorised(BaseException):
    pass


class ExpectationFailure(BaseException):
    pass


class FileReadFailed(BaseException):
    pass


class FileNameError(BaseException):
    pass


class MaxOccurrenceError(BaseException):
    pass


class CreateFolderError(BaseException):
    pass
