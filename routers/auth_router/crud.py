from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI
from sqlalchemy import DateTime
from . import models, schemas
from typing import Optional
from datetime import date
from uuid import UUID


async def create_deadline(deadline_type, start_date, ending, db:Session):
    res = db.execute("""insert into public.deadline(deadline_type,start_date,ending)
    values(:deadline_type, :start_date, :ending) """,
    {'deadline_type':deadline_type, 'start_date':start_date, 'ending':ending})
    db.commit()
    return res

async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id FROM public.deadline; """)
    res = res.fetchall()
    return res

async def update_deadline(deadline: schemas.update_deadline, db: Session):
    res = db.execute("""UPDATE public.deadline
	SET deadline_id = :deadline_id, deadline_type = :deadline_type, start_date = :start_date, ending = :ending
	WHERE deadline_id = :deadline_id;""",
    {'deadline_id':deadline.deadline_id, 'deadline_type':deadline.deadline_type, 'start_date':deadline.start_date, 'ending':deadline.ending})
    db.commit()
    return res

async def delete_deadline(deadline: schemas.delete_deadline, db: Session):
    res = db.execute("""DELETE FROM public.deadline
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline.deadline_id})
    db.commit()
    return res    

async def create_staff(fname, sname, oname, email, supervisor, gender, role, department, positions, grade, appointment, db:Session):
    try:
        res = db.execute("""insert into public.staff(fname, sname, oname, email, supervisor, gender, role, department, positions, grade, appointment)
        VALUES(:fname, :sname, :oname, :email, :supervisor, :gender, :role, :department, :positions, :grade, :appointment)""",
        {'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'role':role, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment})
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res


async def read_staff(db:Session):
    res = db.execute(""" SELECT staff_id, fname, sname, oname, email, supervisor, gender, role, department, positions, grade, appointment FROM public.staff; """)
    res = res.fetchall()
    return res

async def update_staff(staff_id, fname, sname, oname, email, supervisor, gender, role, department, positions, grade, appointment, db:Session):
    res = db.execute("""UPDATE public.staff
    SET staff_id = :staff_id, fname = :fname, sname = :sname, oname = :oname, email = :email, supervisor = :supervisor, gender = :gender, role = :role, department = :department, positions = :positions, grade = :grade, appointment = :appointment
    WHERE staff_id = :staff_id;""",
    {'staff_id':staff_id, 'fname':fname, 'sname':sname, 'oname':oname, 'email':email, 'supervisor':supervisor, 'gender':gender, 'role':role, 'department':department, 'positions':positions, 'grade':grade, 'appointment':appointment})
    db.commit()
    return res

async def delete_staff(staff:schemas.delete_staff, db: Session):
    res = db.execute("""DELETE FROM public.staff 
	WHERE staff_id = :staff_id;""",
    {'staff_id':staff.staff_id})
    db.commit()
    return res


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

async def delete_user(db: Session,id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return user + 'not found'
    db.delete(user)
    db.commit()
    return user + 'deleted'




    


