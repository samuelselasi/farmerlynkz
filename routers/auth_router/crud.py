from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI
from . import models, schemas
from typing import Optional
from uuid import UUID
from sqlalchemy import DateTime
from datetime import date


async def create_deadline( deadline: schemas.create_deadline, db:Session):
    res = db.execute(""" INSERT INTO public.deadline(type, start_date, ending) VALUES (:type, :start_date, :ending); """,{'type':deadline.type, 'start_date':deadline.start_date, 'ending':deadline.ending})
    db.commit()
    return res

async def read_deadline_table(db:Session):
    res = db.execute(""" select * from deadline """)
    res = res.fetchall()
    return res

async def create_staff( user: schemas.UserCreate, db:Session):
    res = db.execute("""INSERT INTO public.staff(fname, sname, oname, email, supervisor, gender, role, department, position, grade) VALUES (:fname, :sname, :oname, :email, :supervisor, :gender, :role, :department, :position, :grade);""",{'fname':user.fname, 'sname':user.sname, 'oname':user.oname, 'email':user.email, 'supervisor':user.supervisor, 'gender':user.gender, 'role':user.role, 'department':user.department, 'position':user.position, 'grade':user.grade})
    db.commit()
    return res

async def read_staff(db:Session):
    res = db.execute(""" select * from staff """)
    res = res.fetchall()
    return res

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




    


