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

@router.get("/roles/")
async def read_roles(db: Session = Depends(get_db)):
    return await crud.read_roles(db)

@router.get("/deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)

@router.get("/deadline/start/")
async def read_start_deadline(db: Session = Depends(get_db)):
    return await crud.read_start_deadline_table(db)

@router.get("/deadline/mid/")
async def read_mid_deadline(db: Session = Depends(get_db)):
    return await crud.read_mid_deadline_table(db)

@router.get("/deadline/end/")
async def read_end_deadline(db: Session = Depends(get_db)):
    return await crud.read_end_deadline_table(db)


@router.post("/")
async def create_staff(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_staff(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, db)

@router.post("/roles/")
async def create_roles(payload: schemas.create_roles, db: Session = Depends(get_db)):
    return await crud.create_roles(payload.role_description, db)

@router.post("/deadline/")
async def create_deadline(payload:schemas.create_deadline, db: Session = Depends(get_db) ):
    return await crud.create_deadline(payload.deadline_type, payload.start_date, payload.ending, db)


@router.put("/")
async def update_staff(payload: schemas.update_staff, db:Session = Depends(get_db)):
    return await crud.update_staff(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles,  db)

@router.put("/roles/")
async def update_roles(payload: schemas.update_roles, db:Session = Depends(get_db)):
    return await crud.update_roles(payload.role_id, payload.role_description, db)

@router.put("/Deadline/")
async def update_deadline_table(deadline: schemas.update_deadline, db: Session = Depends(get_db)):
    return await crud.update_deadline(deadline, db)


@router.delete("/{staff_id}/")
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    return await crud.delete_staff(staff_id, db)
  
@router.delete("/{role_id}/")
async def delete_roles(role_id: int, db: Session = Depends(get_db)):
    return await crud.delete_roles(role_id, db)
  
@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    return await crud.delete_deadline(deadline_id, db)    
