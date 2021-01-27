from datetime import datetime, time, timedelta
from typing import List, Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime
# from sqlalchemy import DateTime

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int


class DeadlineTable(BaseModel):
    title: Optional[str]
    metatitle: Optional[datetime.datetime]
    body: Optional[datetime.datetime]


class create_deadline(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    end_date: DeadlineTable


class read_deadline_table(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    end_date: DeadlineTable