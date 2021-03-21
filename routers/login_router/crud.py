from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import schema, hashpassword, model
# from login_router.model import User_list
# from login_router.schema import UserInDb
# from login_router.hashpassword import get_password_hash


def findByEmail(email: EmailStr, db: Session):
    return db.query(model.User_list).filter(model.User_list.email == email).first()


def findByusername(username: str, db: Session):
    return db.query(model.User_list).filter(model.User_list.username == username).first()


def create_user(db: Session, user: schema.UserInDb):
    hashPassword = hashpassword.get_password_hash(user.password)
    db_user = model.User_list(
        email=user.email, username=user.username, password=hashPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
