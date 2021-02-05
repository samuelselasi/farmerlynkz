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
SECRET = "appraisal_secret"
from fastapi import Depends
from typing import Optional
from . import crud, schemas
from main import get_db
from uuid import UUID


manager = LoginManager(SECRET, tokenUrl='/auth/token')

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

fake_db = {'johndoe@e.mail': {'password': 'hunter2'}}


@manager.user_loader
def load_user(email: str):  
    user = fake_db.get(email)
    return user

@router.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  
    if not user:
        raise InvalidCredentialsException  
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post("/create/staff")
async def create_staff(user:schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_staff(user, db)
   
@router.get("staff/")
async def read_staff(db: Session = Depends(get_db)):
    return await crud.read_staff(db)

@router.put("/update/staff")
async def update_staff(staff:schemas.update_staff, db:Session = Depends(get_db)):
    return await crud.update_staff(staff, db)

@router.delete("/staff/")
async def delete_staff(staff: schemas.delete_staff, db: Session = Depends(get_db)):
    return await crud.delete_staff(staff, db)
  
@router.post("/deadline")
async def create_deadline(deadline:schemas.create_deadline, db: Session = Depends(get_db) ):
    return await crud.create_deadline(deadline, db)

@router.get("/deadline/list")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)

@router.put("/deadline/table")
async def update_deadline_table(deadline: schemas.update_deadline_table, db: Session = Depends(get_db)):
    return await crud.update_deadline_table(deadline, db)

@router.delete("/deadline/")
async def delete_deadline(deadline: schemas.delete_deadline, db: Session = Depends(get_db)):
    return await crud.delete_deadline(deadline, db)    

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.delete("/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    return await crud.delete_user(db, id)

@router.put("/update/{id}")
async def update_user(id: int, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.update_user(db,id,payload)    \

@router.get("/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
    return await crud.get_user(db, id)

@router.get("/")
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    return await crud.get_users(db,skip,limit,search,value)