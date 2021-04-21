from fastapi import APIRouter, Depends, BackgroundTasks
from main import get_db, oauth2_scheme
from . import crud, schemas, models
from sqlalchemy.orm import Session



router = APIRouter()


# READ AUTH DETAILS

@router.get("/", response_model=schemas.User)
async def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.get_current_user(token, db)

# USER LOGIN/LOGOUT

@router.post("/login", description="authenticate user details", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db:Session=Depends(get_db)):
    return await crud.authenticate(payload, db)

@router.post("/logout", description="revoke token")
async def logout(payload:schemas.Token, db:Session=Depends(get_db)):
    return await crud.revoke_token(payload, db)

# REFRESH ACCESS TOKEN

@router.post("/refresh", description="refresh user access/refresh tokens", response_model=schemas.Token)
async def refresh_token(payload: schemas.Token, db: Session=Depends(get_db)):
    return await crud.refresh_token(payload, db)

# RESET PASSWORD

@router.post("/request", description="authenticate user details")
async def request_password_reset(payload:schemas.UserBase, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    return await crud.request_password_reset(payload, db, background_tasks)

@router.post("/request_", description="authenticate user details")
async def request_password_reset_(payload:schemas.UserBase, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    return await crud.request_password_reset_(payload, db, background_tasks)