from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db

from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Body, FastAPI




router = APIRouter()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")



@router.post("/authenticate")
async def login(payload:schemas.UserCreate, db:Session=Depends(get_db)):
    return await crud.login(payload, db)



@router.get("/")
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    return await crud.get_users(db,skip,limit,search,value)



@router.get("/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
    return await crud.get_user(db, id)
     


@router.post("/create")
async def create_users(user:schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = await crud.create_user(user,db)
    return new_user



@router.delete("/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    return await crud.delete_user(db, id)



@router.put("/update/{id}")
async def update_user(id: int, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.update_user(db,id,payload)


@router.post("/deadline/")
async def create_deadline(payload:List[schemas.CreateDeadlineTable], db: Session = Depends(get_db)):
    return await crud.create_deadline(payload,db)

@router.get("/")
async def read_deadline_table(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    return await crud.read_deadline_table(db,skip,limit,search,value)