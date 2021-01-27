from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, time, timedelta
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Body, FastAPI
from typing import Optional
from . import crud, schemas
from main import get_db
from uuid import UUID


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

@router.post("/create_deadline")
async def create_deadline(db: Session = Depends(get_db)):
    return await crud.create_deadline(db)

@router.get("read_deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)