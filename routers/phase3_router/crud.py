from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException, jwt
from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import email

# READ END OF YEAR REVIEW


async def read_annual_appraisal(db: Session):
    res = db.execute("""SELECT * FROM public.annual_appraisal;""")
    res = res.fetchall()
    return res


async def read_competence_details(db: Session):
    res = db.execute("""SELECT * FROM public.competence_details;""")
    res = res.fetchall()
    return res


async def read_performance_details(db: Session):
    res = db.execute("""SELECT * FROM public.performance_details;""")
    res = res.fetchall()
    return res


# CREATE END OF YEAR REVIEW

async def create_annual_appraisal(payload: schemas.AnnualAppraisal, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.annual_appraisal(
	                    result_areas, target, resources, appraisal_form_id, submit)
	                    values(:result_areas, :target, :resources, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do 
	                    update set result_areas = EXCLUDED.result_areas, target = EXCLUDED.target, resources = EXCLUDED.resources, submit = EXCLUDED.submit; """,
                         {'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.start.approve_annual_plan(payload.appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "annual plan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def competence_details(competence_id, grade, submit, appraisal_form_id, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.competence_details(competence_id, grade, submit, appraisal_form_id)
	                     values(:competence_id, :grade, :comment, :submit, :appraisal_form_id) on conflict (appraisal_form_id) do 
	                    update set competence_id = EXCLUDED.competence_id, grade = EXCLUDED.grade, submit = EXCLUDED.submit; """,
                         {'competence_id': competence_id, 'grade': grade, 'submit': submit, 'appraisal_form_id': appraisal_form_id})  # CREATE INTO TABLE
        db.commit()
        if submit == 1:
            # SEND COMPETENCE DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.start.approve_annual_plan(appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "competence details has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def performance_details(assessment, final_score, weight, comment, submit,  approval_date, appraisal_form_id, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.competence_details(competence_id, grade, submit, appraisal_form_id)
	                     values(:competence_id, :grade, :comment, :submit, :appraisal_form_id) on conflict (appraisal_form_id) do 
	                    update set competence_id = EXCLUDED.competence_id, grade = EXCLUDED.grade, submit = EXCLUDED.submit; """,
                         {'assessment': assessment, 'final_score': final_score, 'weight': weight, 'comment': comment, 'submit': submit, 'approval_date': approval_date, 'appraisal_form_id': appraisal_form_id})  # CREATE INTO TABLE
        db.commit()
        if submit == 1:
            # SEND PERFORMANCE PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.start.approve_annual_plan(appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "competence details has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})
