from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from . import crud, auth, login_db, model, schema
# from login_router.crud import findByEmail, findByusername
# from login_router.auth import NotConfirmPassword
# from login_router.db import get_db
# from login_router.crud import create_user
# from login_router.schema import LoginUser, SignupUser


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_User(user: schema.SignupUser, db: Session = Depends(login_db.get_db)):
    if(crud.findByEmail(user.email, db) != None):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already taken")
    if(crud.findByusername(user.username, db) != None):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already taken")
    if(auth.NotConfirmPassword(user.password, user.confirmPassword)):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="confirm Password doesnot match with Password")
    dbuser = crud.create_user(db, user)
    return {
        "success": "OK",
        "user": dbuser}  # Testing er jono I have to remove this


@router.post("/login")
async def login_User(user: schema.LoginUser, db: Session = Depends(login_db.get_db)):

    # else:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
