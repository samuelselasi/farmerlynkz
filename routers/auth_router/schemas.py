from typing import List, Optional
from pydantic import BaseModel

from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Body, FastAPI





class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int


class DeadlineTable(BaseModel):
    title: Optional[str]
    metatitle: Optional[datetime]
    body: List[datetime]


class CreateDeadlineTable(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    end_date: DeadlineTable


class read_deadline_table(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    end_date: DeadlineTable