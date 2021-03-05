from fastapi import Depends, HTTPException, Response, status, Body, Header
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI
from sqlalchemy import DateTime
from . import models, schemas
from typing import Optional
from datetime import date
from uuid import UUID




async def read_staff(db:Session):
    res = db.execute(""" SELECT public.get_staff(); """)
    res = res.fetchall()
    return res

async def read_roles(db:Session):
    res = db.execute(""" SELECT role_id, role_description FROM public.roles; """)
    res = res.fetchall()
    return res

async def create_staff(fname, sname, oname, email, supervisor, gender, roles, department, positions, grade, appointment, db:Session):
    res = db.execute("""insert into public.staff(fname, sname, oname, email, supervisor, gender, roles, department, positions, grade, appointment)
    VALUES(:fname, :sname, :oname, :email, :supervisor, :gender, :roles, :department, :positions, :grade, :appointment)""",
    {'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'roles':roles, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment})
    db.commit()
    return res

async def create_roles(role_description, db:Session):
    res = db.execute(""" INSERT INTO public.roles(role_description) VALUES(:role_description) """, {'role_description': role_description})
    db.commit()
    return res

async def update_staff(staff_id, fname, sname, oname, email, supervisor, gender, roles, department, positions, grade, appointment, db:Session):
    res = db.execute("""UPDATE public.staff
    SET staff_id = :staff_id, fname = :fname, sname = :sname, oname = :oname, email = :email, supervisor = :supervisor, gender = :gender, roles = :roles, department = :department, positions = :positions, grade = :grade, appointment = :appointment
    WHERE staff_id = :staff_id;""",
    {'staff_id':staff_id, 'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'roles':roles, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment})
    db.commit()
    return res

async def update_roles(role_id, role_description, db:Session):
    res = db.execute(""" UPDATE public.roles SET role_id = :role_id, role_description = :role_description WHERE role_id = :role_id; """,
    {'role_id':role_id, 'role_description': role_description})
    db.commit()
    return res

async def delete_staff(staff_id:int, db: Session):
    res = db.execute("""DELETE FROM public.staff 
	WHERE staff_id = :staff_id;""",
    {'staff_id':staff_id})
    db.commit()
    return res

async def delete_roles(role_id:int, db: Session):
    res = db.execute(""" DELETE FROM public.roles WHERE role_id = :role_id; """, {'role_id':role_id})
    db.commit()
    return res



    


