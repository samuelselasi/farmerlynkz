from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends


async def read_appraiser_appraisees(user_id, db: Session):
    res = db.execute(""" select get_list_of_appraisee(:user_id) """,{'user_id':user_id})
    return res.fetchall()

async def read_completed_list(user_id:int, deadline:str, db:Session):
    res = db.execute("""SELECT public.get_list_of_completed_form(:deadline, :user_id)""",{'user_id':user_id, 'deadline':deadline})
    res = res.fetchall()
    return res    

async def read_incomplete_list(user_id:int, deadline:str, db:Session):
    res = db.execute("""SELECT public.get_list_of_incomplete_form(:deadline, :user_id)""",{'user_id':user_id, 'deadline':deadline})
    res = res.fetchall()
    return res    