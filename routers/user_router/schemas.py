from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    password: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    # phone: Optional[str]
    user_type_id: int
    status: Optional[bool]
class UserUpdate(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    # phone: Optional[str]
class ResetPassword(BaseModel):
    password: str
    code: Optional[str]
class ChangePassword(BaseModel):
    email: str
    password: str
    confirm_password: str
class UserInfo(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    # phone: Optional[str]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True
class User(UserBase):
    id: int
    user_type_id: int
    user_info : UserInfo
    
    class Config:
        orm_mode = True
    