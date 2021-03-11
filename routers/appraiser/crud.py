from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends


async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """)
    res = res.fetchall()
    return res

async def read_appraiser_appraisees(user_id, db: Session):
    res = db.execute(""" SELECT public.get_list_of_appraisee(:user_id) """,{'user_id':user_id})
    return res.fetchall()  

async def read_completed_list(deadline:str, user_id:int, db:Session):
    res = db.execute("""SELECT public.get_list_of_approved_form(:deadline, :user_id)""",{'deadline':deadline, 'user_id':user_id})
    res = res.fetchall()
    return res 

async def read_approved_forms(deadline:str, user_id:int, db:Session):
    res = db.execute("""SELECT public.get_list_of_approved_form(:deadline, :user_id)""",{'deadline':deadline, 'user_id':user_id})
    res = res.fetchall()
    return res 

async def waiting_approval_list(deadline:str, user_id:int, db:Session):
    res = db.execute("""SELECT public.get_list_of_waiting_approval(:deadline, :user_id)""",{'deadline':deadline, 'user_id':user_id})
    res = res.fetchall()
    return res 

async def read_incomplete_list(deadline:str, user_id:int, db:Session):
    res = db.execute("""SELECT public.get_list_of_incompleted_form(:deadline, :user_id)""",{'deadline':deadline, 'user_id':user_id})
    res = res.fetchall()
    return res    

async def read_supervisors(db: Session):
    res = db.execute(""" SELECT public.get_view_supervisors() """)
    res = res.fetchall()
    return res

async def read_yearly_form_deatails(staff_id:int, form_year: int, db:Session):
    res = db.execute(""" SELECT public.get_form_details_yearly(:staff_id, :form_year) """, {'staff_id':staff_id, 'form_year':form_year})
    res = res.fetchall()
    return res

async def approve_form(appraisal_form_id: int, type_form: str, db: Session):
    res = db.execute(""" SELECT public.approve_form_details (:appraisal_form_id, :type_form) """, {'appraisal_form_id': appraisal_form_id, 'type_form': type_form})
    res = res.fetchall()
    return res


async def create_deadline(deadline_type, start_date, ending, db:Session):
    res = db.execute("""insert into public.deadline(deadline_type,start_date,ending)
    values(:deadline_type, :start_date, :ending) """,
    {'deadline_type':deadline_type, 'start_date':start_date, 'ending':ending})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been created"})



async def update_deadline(deadline: schemas.update_deadline, db: Session):
    res = db.execute("""UPDATE public.deadline
	SET deadline_id = :deadline_id, deadline_type = :deadline_type, start_date = :start_date, ending = :ending
	WHERE deadline_id = :deadline_id;""",
    {'deadline_id':deadline.deadline_id, 'deadline_type':deadline.deadline_type, 'start_date':deadline.start_date, 'ending':deadline.ending})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been updated"})



async def delete_deadline(deadline_id: int, db: Session):
    res = db.execute("""DELETE FROM public.deadline
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline.deadline_id})
    db.commit() 
    return JSONResponse(status_code=200, content={"message": "deadline has been deleted"})