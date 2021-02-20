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
# SECRET = "appraisal_secret"
from fastapi import Depends
from typing import Optional
from . import crud, schemas
from main import get_db
from uuid import UUID


# manager = LoginManager(SECRET, tokenUrl='/auth/token')

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")



@router.get("/")
async def read_staff(db: Session = Depends(get_db)):
    return await crud.read_staff(db)

@router.get("/Deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)



@router.post("/")
async def create_staff(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_staff(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.role, payload.department, payload.positions, payload.grade, payload.appointment, db)

@router.post("/Deadline/")
async def create_deadline(payload:schemas.create_deadline, db: Session = Depends(get_db) ):
    return await crud.create_deadline(payload.deadline_type, payload.start_date, payload.ending, db)



@router.put("/")
async def update_staff(payload: schemas.update_staff, db:Session = Depends(get_db)):
    return await crud.update_staff(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.role, payload.department, payload.positions, payload.grade, payload.appointment, db)

@router.put("/Deadline/")
async def update_deadline_table(deadline: schemas.update_deadline, db: Session = Depends(get_db)):
    return await crud.update_deadline(deadline, db)



@router.delete("/{staff_id}/")
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    return await crud.delete_staff(staff_id, db)
  
@router.delete("/Deadline/{deadline_id}/")
async def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    return await crud.delete_deadline(deadline_id, db)    

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# @router.delete("/delete/{id}")
# async def delete_user(id: int, db: Session = Depends(get_db)):
#     return await crud.delete_user(db, id)

# @router.get("/{id}")
# async def read_user(id: int, db: Session = Depends(get_db)):
#     return await crud.get_user(db, id)

# @router.get("/")
# async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
#     return await crud.get_users(db,skip,limit,search,value)

# //////////////////////////////////////
# @manager.user_loader
# def load_user(email: str):  
#     user = fake_db.get(email)
#     return user

# @router.post('/auth/token')
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password

#     user = load_user(email)  
#     if not user:
#         raise InvalidCredentialsException  
#     elif password != user['password']:
#         raise InvalidCredentialsException

#     access_token = manager.create_access_token(
#         data=dict(sub=email)
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}