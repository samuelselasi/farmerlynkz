from fastapi import APIRouter, Depends, HTTPException, Body, FastAPI
from datetime import datetime, time, timedelta
from main import get_db, oauth2_scheme
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from uuid import UUID


router = APIRouter()

# READ STAFF DETAILS
@router.get("/staffopen/")
async def read_staff(db:Session=Depends(get_db)):
    return await crud.read_staff(db)

@router.get("/staff/")
async def read_staff(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_staff_auth(token, db)

@router.get("/supervisorsopen/")
async def read_supervisors(db:Session=Depends(get_db)):
    return await crud.read_supervisors(db)

@router.get("/supervisors/")
async def read_supervisors(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_supervisors_auth(token, db)

@router.get("/{name}open/")
async def read_staff_by_name(name:str, db:Session=Depends(get_db)):
    return await crud.read_staff_by_name(name, db)

@router.get("/{name}/")
async def read_staff_by_name(name:str, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_staff_by_name_auth(name, token, db)

@router.get("/rolesopen/")
async def read_roles(db:Session=Depends(get_db)):
    return await crud.read_roles(db)

@router.get("/roles/")
async def read_roles(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_roles_auth(token, db)

@router.get("/deadlineopen/")
async def read_deadline_table(db:Session=Depends(get_db)):
    return await crud.read_deadline_table(db)

@router.get("/deadline/")
async def read_deadline_table(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_deadline_table_auth(token, db)

@router.get("/deadlinestartopen/")
async def read_start_deadline(db:Session=Depends(get_db)):
    return await crud.read_start_deadline_table(db)

@router.get("/deadlinestart/")
async def read_start_deadline(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_start_deadline_table_auth(token, db)

@router.get("/deadline/mid/")
async def read_mid_deadline(db:Session=Depends(get_db)):
    return await crud.read_mid_deadline_table(db)

@router.get("/deadline/end/")
async def read_end_deadline(db:Session=Depends(get_db)):
    return await crud.read_end_deadline_table(db)


# DEACTIVATE STAFF 
@router.get("/deactivatestaff/{staff_id}/open/")
async def deactivate_staff(staff_id:int, db:Session=Depends(get_db)):
    return await crud.deactivate_staff(staff_id, db)

@router.get("/deactivatestaff/{staff_id}/")
async def deactivate_staff(staff_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.deactivate_staff_auth(staff_id, token, db)


# CREATE STAFF DETAILS
@router.post("/staffopen/")
async def create_staff(payload:schemas.UserCreate, db:Session=Depends(get_db)):
    return await crud.create_staff(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, db)

@router.post("/staff/")
async def create_staff(payload:schemas.UserCreate, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.create_staff_auth(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, token, db)

@router.post("/rolesopen/")
async def create_roles(payload:schemas.create_roles, db:Session=Depends(get_db)):
    return await crud.create_roles(payload.role_description, db)

@router.post("/roles/")
async def create_roles(payload:schemas.create_roles, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.create_roles_auth(payload.role_description, token, db)

@router.post("/deadlineopen/")
async def create_deadline(payload:schemas.create_deadline, db:Session=Depends(get_db) ):
    return await crud.create_deadline(payload.deadline_type, payload.start_date, payload.ending, db)

@router.post("/deadline/")
async def create_deadline(payload:schemas.create_deadline, token:str=Depends(oauth2_scheme), db: Session=Depends(get_db) ):
    return await crud.create_deadline_auth(payload.deadline_type, payload.start_date, payload.ending, token, db)


# UPDATE STAFF DETAILS
@router.put("/staffopen/")
async def update_staff(payload:schemas.update_staff, db:Session=Depends(get_db)):
    return await crud.update_staff(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles,  db)

@router.put("/staff/")
async def update_staff(payload:schemas.update_staff, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_staff_auth(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, token, db)

@router.put("/Deadlineopen/")
async def update_deadline_table(deadline:schemas.update_deadline, db:Session=Depends(get_db)):
    return await crud.update_deadline(deadline, db)

@router.put("/Deadline/")
async def update_deadline_table(deadline:schemas.update_deadline, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_deadline_auth(deadline, token, db)

@router.put("/rolesopen/")
async def update_roles(payload:schemas.update_roles, db:Session=Depends(get_db)):
    return await crud.update_roles(payload.role_id, payload.role_description, db)

@router.put("/roles/")
async def update_roles(payload:schemas.update_roles, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_roles_auth(payload.role_id, payload.role_description, token, db)


# DELETE STAFF DETAILS
@router.delete("/{staff_id}/open/")
async def delete_staff(staff_id:int, db:Session=Depends(get_db)):
    return await crud.delete_staff(staff_id, db)

@router.delete("/{staff_id}/")
async def delete_staff(staff_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_staff_auth(staff_id, token, db)

@router.delete("/{role_id}/open")
async def delete_roles(role_id:int, db:Session=Depends(get_db)):
    return await crud.delete_roles(role_id, db)

@router.delete("/{role_id}/")
async def delete_roles(role_id:int, tken:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_roles_auth(role_id, token, db)

@router.delete("/deadline/{deadline_id}/open/")
async def delete_deadline(deadline_id:int, db:Session=Depends(get_db)):
    return await crud.delete_deadline(deadline_id, db)    

@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_deadline_auth(deadline_id, token, db) 