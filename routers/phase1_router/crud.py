from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import services

 
async def read_appraisal_form(db:Session):
    res = db.execute("""SELECT department, grade, positions, appraisal_form_id, date, staff_id FROM public.appraisal_form;""")
    res = res.fetchall()
    return res

async def read_annual_plan(db:Session):
    res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id
	FROM public.annual_plan;""")
    res = res.fetchall()
    return res

async def read_annual_appraisal(db:Session):
    res = db.execute("""SELECT public.get_appraisal_form();""")
    res = res.fetchall()
    return res

async def verify_hash_form(hash_:str, db:Session):
    res = db.execute(""" SELECT public.get_hash_verification(:hash_) """,{'hash_':hash_})
    res = res.fetchall()
    return res

async def read_hash_form(db:Session):
    res = db.execute("""SELECT public.get_entire_hash_table();""")
    res = res.fetchall()
    return res

async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """)
    res = res.fetchall()
    return res


async def appraisal_form(department, grade, positions, date, staff_id, db:Session):
    res = db.execute("""insert into public.appraisal_form(department, grade, positions, date, staff_id)
    values(:department, :grade, :positions, :date, :staff_id);""",
    {'department':department, 'grade':grade, 'positions':positions, 'date':date, 'staff_id':staff_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been created"})

async def create_annual_plan(result_areas, target, resources, appraisal_form_id, db:Session):
    query = db.execute(""" SELECT ending FROM public.deadline WHERE deadline_type = 'Start'; """)
    query = query.first()[0]
    if query >= date.today():
        res = db.execute("""INSERT INTO public.annual_plan(
	                    result_areas, target, resources, appraisal_form_id)
	                    values(:result_areas, :target, :resources, :appraisal_form_id) on conflict (appraisal_form_id) do 
	                    update set result_areas = EXCLUDED.result_areas, target = EXCLUDED.target, resources = EXCLUDED.resources; """,
                        {'result_areas':result_areas, 'target':target,'resources':resources, 'appraisal_form_id':appraisal_form_id})
        db.commit()
        await services.main.approve_annual_plan()
        
    #     return JSONResponse(status_code=200, content={"message": "annual plan has been created"})
    # else:
    #     return JSONResponse(status_code=404, content={"message": "deadline has passed!"})
            
async def create_annual_appraisal(comment, field, appraisal_form_id, db:Session):
    res = db.execute("""insert into public.annual_appraisal(comment, field, appraisal_form_id)
    values(:comment, :field, :appraisal_form_id);""",
    {'comment':comment,'field':field, 'appraisal_form_id':appraisal_form_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been created"})

async def create_appraisal_form(deadline, department, positions, grade, date, staff_id, progress_review, remarks, assessment, score, weight, comment, db:Session):
    res = db.execute("""SELECT public.create_appraisal_form(deadline:deadline, department:department, positions:positions, grade:grade, date:date, staff_id:staff_id, progress_review:progress_review, remarks:remarks, assessment:assessment, score:score, weight:weight, comment:comment);""",
    {'deadline':deadline, 'department':department, 'positions':positions, 'grade':grade, 'date':date, 'staff_id':staff_id, 'progress_review':progress_review, 'remarks':remarks, 'assessment':assessment, 'score':score, 'weight':weight, 'comment':comment})
    db.commit()
    return res


async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session):
    res = db.execute("""UPDATE public.appraisal_form
	SET appraisal_form_id = :appraisal_form_id, department = :department, grade = :grade, position = :positions, date = :date, staff_id = :staff_id
	WHERE appraisal_form_id = :appraisal_form_id;""",
    {'appraisal_form_id':appraisal_form.appraisal_form_id, 'department': appraisal_form.department, 'grade': appraisal_form.grade, 'positions': appraisal_form.positions, 'date': appraisal_form.date, 'staff_id': appraisal_form.staff_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been updated"})

async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session):
    res = db.execute("""UPDATE public.annual_plan 
    SET result_areas = :result_areas, target = :target, resources = :resources, appraisal_form_id = :appraisal_form_id, annual_plan_id = :annual_plan_id
	WHERE annual_plan_id = :annual_plan_id;""", 
    {'result_areas':annual_plan.result_areas, 'target':annual_plan.target,'resources':annual_plan.resources, 'appraisal_form_id':annual_plan.appraisal_form_id, 'annual_plan_id':annual_plan.annual_plan_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual plan has been updated"})

async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
    res = db.execute("""UPDATE public.annual_appraisal
	SET comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been updated"})


async def delete_appraisal_form(appraisal_form_id: int, db:Session):
    res = db.execute("""DELETE FROM public.appraisal_form
	WHERE appraisal_form_id = :appraisal_form_id;""",
    {'appraisal_form_id': appraisal_form_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been deleyed"})

async def delete_annual_plan(annual_plan_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_plan
	WHERE annual_plan_id = :annual_plan_id;""",
    {'annual_plan_id': annual_plan_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual plan has been deleted"})

async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_appraisal
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'annual_appraisal_id':annual_appraisal_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been deleted"})

