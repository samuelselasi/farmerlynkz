from ..user_router.schemas import UserBase, User
from pydantic import BaseModel
from typing import Optional


class Auth(UserBase):
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


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
