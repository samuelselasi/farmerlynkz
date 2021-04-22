from fastapi import APIRouter, Depends, HTTPException, Response, status
from main import get_db, oauth2_scheme
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from main import get_db

router = APIRouter()


# GET USER DETAILS
@router.get("/", description="get all users", response_model=List[schemas.User])
async def read_users(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_users_auth(token, db)

@router.get("/{id}", description="get user by id", response_model=schemas.User)
async def read_user_by_id(id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    user = await crud.read_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return user

@router.get("/{email}/", description="get user by email", response_model=schemas.User)
async def read_user_by_email(email:str, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    user = await crud.read_user_by_email_auth(email, token, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with email: {} was not found".format(email))
    return user


@router.get("/read/hash/")
async def verify_hash_details(code:str, db:Session=Depends(get_db)):
    return await crud.read_hash_code(code, db)

@router.get("/read/hash/table/")
async def read_hash_table(db:Session=Depends(get_db)):
    return await crud.read_hash_table(db)


# CREATE USER DETAILS
@router.post("/", description="create user", response_model=schemas.User)
async def create_user(payload:schemas.UserCreate, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.create_user_auth(payload, token, db)


# UPDATE USER DETAILS
@router.patch("/update/{id}", description="update user by id", response_model=schemas.User, status_code=202)
async def update_user(id:int, payload:schemas.UserUpdate, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_user_auth(id, payload, token, db)


# DELETE USER DETAILS
@router.delete("/{id}", description="delete user by id")
async def delete_user(id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_user_auth(id, token, db)
    
@router.post("/verify/password", description="verify user password")
async def verify_password(id:int, payload:schemas.ResetPassword, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.verify_password_auth(id, payload, token, db)

@router.patch("/{id}/password", description="change user password", status_code=status.HTTP_202_ACCEPTED)
async def update_password(id:int, payload:schemas.ResetPassword, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.reset_password_auth(id, payload, token, db)

# @router.patch("/{id}/password_", description="change user password", status_code=status.HTTP_202_ACCEPTED)
# async def update_password(id:int, payload:schemas.ResetPassword, db:Session=Depends(get_db)):
#     return await crud.reset_password(id, payload, db)

@router.patch("/password", description="change user password", status_code=status.HTTP_202_ACCEPTED)
async def update_password_(email:str, payload:schemas.ResetPassword, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.reset_password_auth(email, payload, token, db)

@router.put("/change/password")
async def change_password(email:str, password:str, db:Session=Depends(get_db)):
    return await crud.change_password(email, password, db)