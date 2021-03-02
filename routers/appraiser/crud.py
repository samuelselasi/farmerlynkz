from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends


async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id FROM public.deadline; """)
    res = res.fetchall()
    return res


async def read_appraiser_appraisees(user_id, db: Session):
    res = db.execute(""" select get_list_of_appraisee(:user_id) """,{'user_id':user_id})
    return res.fetchall()

async def read_completed_list(user_id:int, deadline:str, db:Session):
    res = db.execute("""SELECT public.get_list_of_completed_form(:deadline, user_id:=1)""",{'deadline':deadline})
    res = res.fetchall()
    return res    

async def read_incomplete_list(user_id:int, deadline:str, db:Session):
    res = db.execute("""SELECT public.get_list_of_incomplete_form(:deadline, :user_id)""",{'user_id':1, 'deadline':deadline})
    res = res.fetchall()
    return res    

async def create_deadline(deadline_type, start_date, ending, db:Session):
    res = db.execute("""insert into public.deadline(deadline_type,start_date,ending)
    values(:deadline_type, :start_date, :ending) """,
    {'deadline_type':deadline_type, 'start_date':start_date, 'ending':ending})
    db.commit()
    return res

async def update_deadline(deadline: schemas.update_deadline, db: Session):
    res = db.execute("""UPDATE public.deadline
	SET deadline_id = :deadline_id, deadline_type = :deadline_type, start_date = :start_date, ending = :ending
	WHERE deadline_id = :deadline_id;""",
    {'deadline_id':deadline.deadline_id, 'deadline_type':deadline.deadline_type, 'start_date':deadline.start_date, 'ending':deadline.ending})
    db.commit()
    return res

async def delete_deadline(deadline_id: int, db: Session):
    res = db.execute("""DELETE FROM public.deadline
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline.deadline_id})
    db.commit()
    return res  