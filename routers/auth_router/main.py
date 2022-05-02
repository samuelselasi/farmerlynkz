from fastapi import APIRouter, Depends, BackgroundTasks
from . import crud, schemas
# import crud
# import schemas
from sqlalchemy.orm import Session, sessionmaker
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData


router = APIRouter()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sel@localhost:5432/farmerlynkz"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()
db = SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# READ AUTH DETAILS
@router.get("/", response_model=schemas.User)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.get_current_user(token, db)


# USER LOGIN/LOGOUT
@router.post("/login", description="authenticate user details", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db: Session = Depends(get_db)):
    return await crud.authenticate(payload, db)


@router.post("/logout", description="revoke token")
async def logout(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.revoke_token(payload, db)


# REFRESH ACCESS TOKEN
@router.post("/refresh", description="refresh user access/refresh tokens",
             response_model=schemas.Token)
async def refresh_token(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.refresh_token(payload, db)


# RESET PASSWORD
@router.post("/request", description="authenticate user details")
async def request_password_reset(payload: schemas.UserBase,
                                 background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return await crud.request_password_reset_(payload, db, background_tasks)
