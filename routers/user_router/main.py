from fastapi import APIRouter, Depends, HTTPException, Response, status
from main import get_db, oauth2_scheme
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from main import get_db

router = APIRouter()

@router.post("/", description="create user", response_model=schemas.User)
async def create_user(payload:schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(payload,db)

@router.get("/", description="get all users", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db), skip:int=0, limit: int = 100, search:str=None, value:str=None,):
    return await crud.read_users(db,skip,limit,search,value)

@router.get("/{id}", description="get user by id", response_model=schemas.User)
async def read_user_by_id(id: int,db: Session = Depends(get_db)):
    user = await crud.read_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return user

@router.patch("/update/{id}", description="update user by id", response_model=schemas.User, status_code=202)
async def update_user(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    return await crud.update_user(id,payload,db)

@router.delete("/{id}", description="delete user by id")
async def delete_user(id: int, db: Session = Depends(get_db)):
    return await crud.delete_user(id, db)
    
@router.post("/verify/password", description="verify user password")
async def verify_password(id: int, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.verify_password(id, payload, db)

@router.patch("/{id}/password", description="change user password", status_code=status.HTTP_202_ACCEPTED)
async def update_password(id: int, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.reset_password(id,payload,db)
