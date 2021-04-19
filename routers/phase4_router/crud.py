from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from . import schemas

async def read_end_of_year_review(db:Session):
    res = db.execute("""SELECT assessment, score, comment, appraisal_form_id, endofyear_review_id, annual_plan_id, weight
	FROM public.endofyear_review;""")
    res = res.fetchall()
    return res
 
async def read_core_competencies(db:Session):
    res = db.execute("""SELECT category, weight, sub, main, competency_id, annual_appraisal_id, grade
	FROM public.competency;""")
    res = res.fetchall()
    return res

async def read_annual_appraisal(db:Session):
    res = db.execute("""SELECT comment, field, appraisal_form_id, status, annual_appraisal_id FROM public.annual_appraisal;""")
    res = res.fetchall()
    return res


async def create_end_of_year_review(assessment, score, comment, appraisal_form_id, annual_plan_id, weight, staff_id, db: Session):
    res = db.execute("""INSERT INTO public.endofyear_review(assessment, score, comment, appraisal_form_id, annual_plan_id, weight)
    values(:assessment, :score, :comment, :appraisal_form_id, :annual_plan_id, :weight, :staff_id);""",
    {'assessment':assessment, 'score':score, 'comment':comment, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id, 'weight':weight})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "end of year review has been created"})

async def create_core_competencies(annual_appraisal_id, grade, db:Session):
    res = db.execute("""INSERT INTO public.competency(annual_appraisal_id, grade)
    values(:annual_appraisal_id, :grade);""",
    {'annual_appraisal_id':grade, 'grade':grade})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "core competency has been created"})

async def create_annual_appraisal(comment, field, appraisal_form_id, db:Session):
    res = db.execute("""insert into public.annual_appraisal(comment, field, appraisal_form_id)
    values(:comment, :field, :appraisal_form_id);""",
    {'comment':comment,'field':field, 'appraisal_form_id':appraisal_form_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been created"})


async def update_end_of_year_review(end_of_year_review: schemas.update_end_of_year_review, db: Session):
    res = db.execute("""UPDATE public.endofyear_review
	SET assessment = :assessment, score = :score, comment = :comment, appraisal_form_id = :appraisal_form_id, endofyear_review_id = :endofyear_review_id, annual_plan_id = :annual_plan_id, weight = :weight
	WHERE endofyear_review_id = :endofyear_review_id;""",
    {'assessment':assessment, 'score':score, 'comment':comment, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id, 'endofyear_review_id':endofyear_review_id, 'weight':weight})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "end of year review has been updated"})

async def update_core_competencies(core_competencies: schemas.update_core_competencies, db: Session):
    res = db.execute("""UPDATE public.competency
	SET annual_appraisal_id = :annual_appraisal_id, competency_id = :competency_id, grade = :grade
	WHERE competency_id = :competency_id;""",
    {'annual_appraisal_id':annual_appraisal_id, 'competency_id':competency_id, 'grade':grade})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "core competency has been updated"})

async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
    res = db.execute("""UPDATE public.annual_appraisal
	SET grade = comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been updated"})


async def delete_end_of_year_review(endofyear_review_id: int, db: Session):
    res = db.execute("""DELETE FROM public.endofyear_review
	WHERE endofyear_review_id = :endofyear_review_id;""",
    {'endofyear_review_id':endofyear_review_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "end of year review has been deleted"})

async def delete_core_competencies(competency_id: int, db:Session):
    res = db.execute("""DELETE FROM public.competency
	WHERE competency_id = :competency_id;""",
    {'competency_id': competency_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "core competency has been deleted"})

async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_appraisal
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'annual_appraisal_id':annual_appraisal_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been deleted"})
