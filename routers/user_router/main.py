from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas
# import crud
# import schemas
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


router = APIRouter()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sel@localhost:5432/farmerlynkz"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

db = SessionLocal()
# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL USERS
@router.get("/", description="get all users", response_model=List[schemas.User])
async def read_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_users_auth(token, db)

# GET USER BY ID


@router.get("/{id}", description="get user by id", response_model=schemas.User)
async def read_user_by_id(id: int, db: Session = Depends(get_db)):
    user = await crud.read_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=404, detail="user with id: {} was not found".format(id))
    return user

# GET USER BY EMAIL


@router.get("/{email}/", description="get user by email", response_model=schemas.User)
async def getuserbm(email: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await crud.read_user_by_email_auth(email, token, db)
    if not user:
        raise HTTPException(
            status_code=404, detail="user with email: {} was not found".format(email))
    return user


# READ HASH DETAILS
@router.get("/read/hash/")
async def verify_hash_details(code: str, db: Session = Depends(get_db)):
    return await crud.read_hash_code(code, db)

# READ HASH TABLE


@router.get("/read/hash/table/")
async def read_hash_table(db: Session = Depends(get_db)):
    return await crud.read_hash_table(db)


# CREATE USER DETAILS
@router.post("/", description="create user", response_model=schemas.User)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(payload, db)


# UPDATE PASSWORD BY EMAIL


@router.patch("/password/", description="changeuserpassword", status_code=status.HTTP_202_ACCEPTED)
async def update_pwd_(email: str, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.reset_password_(email, payload, db)

# CHANGE PASSWORD(IN USE)


@router.put("/change/password")
async def change_password(payload: schemas.ChangePassword, db: Session = Depends(get_db)):
    return await crud.change_password(payload.email, payload.password, db)


# DELETE USER BY ID
@router.delete("/{id}", description="delete user by id")
async def delete_user(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_user_auth(id, token, db)
