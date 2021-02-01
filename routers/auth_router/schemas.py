from datetime import datetime, time, timedelta
from typing import List, Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy import DateTime

class UserBase(BaseModel):
    staff_id:int
    fname: str
    sname: str
    oname: str
    email: str
    supervisor: int
    gender: str
    role: str
    department: str
    position: str
    grade: int
class UserCreate(UserBase):
    pass
    

class User(UserBase):
    id: int


class DeadlineTable(BaseModel):
    deadline_type: str
    start_date: Optional[datetime.datetime]
    ending: Optional[datetime.datetime]
    deadline_id: int

class create_deadline(DeadlineTable):
    pass


class read_deadline_table(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    ending: DeadlineTable
    deadline_id: DeadlineTable