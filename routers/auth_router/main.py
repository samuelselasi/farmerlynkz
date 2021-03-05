from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, time, timedelta
from fastapi_login import LoginManager
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Body, FastAPI
from fastapi import Depends
from typing import Optional
from . import crud, schemas
from main import get_db
from uuid import UUID


router = APIRouter()


@router.get("/")
async def read_staff(db: Session = Depends(get_db)):
    return await crud.read_staff(db)


@router.post("/")
async def create_staff(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_staff(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.roles, payload.department, payload.positions, payload.grade, payload.appointment, db)


@router.put("/")
async def update_staff(payload: schemas.update_staff, db:Session = Depends(get_db)):
    return await crud.update_staff(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.roles, payload.department, payload.positions, payload.grade, payload.appointment, db)


@router.delete("/{staff_id}/")
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    return await crud.delete_staff(staff_id, db)
  
