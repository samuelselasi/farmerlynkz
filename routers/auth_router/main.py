from fastapi import APIRouter, Depends, BackgroundTasks
from main import get_db, oauth2_scheme
from . import crud, schemas, models
from sqlalchemy.orm import Session
# from typing import List
# import utils, jwt
# , HTTPException, status, BackgroundTasks
# from ..users_router.crud import read_user_by_id

router = APIRouter()

@router.post("/", description="authenticate user details", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db: Session = Depends(get_db)):
    return await crud.authenticate(payload, db)

@router.post("/logout", description="revoke token")
async def logout(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/refresh", description="refresh user access/refresh tokens", response_model=schemas.Token)
async def refresh_token(payload: schemas.Token, db: Session=Depends(get_db)):
    return await crud.refresh_token(payload, db)

@router.post("/request", description="authenticate user details")
async def request_password_reset(payload:schemas.UserBase, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    return await crud.request_password_reset(payload, db, background_tasks)

@router.get("/", response_model=schemas.User)
async def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.get_current_user(token, db)
