from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from . import models, schemas





async def login(payload: schemas.UserCreate, db:Session):
    user = db.query(models.User).filter(models.User.email==payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="{} not found".format(payload.email))

    if models.User.verify_hash(payload.password, user.password):
        return user
    else:
        raise HTTPException(status_code=401)



async def create_user( user: schemas.UserCreate , db: Session):
    db_user = models.User(email=user.email, password=models.User.generate_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



async def get_users(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    base = db.query(models.User)
    if search and value:
        try:
            base = base.filter(models.User.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()



async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()



async def delete_user(db: Session,id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return user + 'not found'
    db.delete(user)
    db.commit()
    return user + 'deleted'



async def update_user(db: Session, id: int, payload: schemas.UserCreate):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return user + 'not found'
    res = db.query(models.User).filter(models.User.id == id).update(payload)
    db.commit()
    return res

