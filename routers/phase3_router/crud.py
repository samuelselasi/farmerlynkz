from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException,jwt
from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import email

# READ END OF YEAR REVIEW
async def read_end_of_year_review(db:Session):
    res = db.execute("""SELECT assessment, score, weight, comment, appraisal_form_id, endofyear_review_id FROM public.endofyear_review;""")
    res = res.fetchall()
    return res
 
async def read_core_competencies(db:Session):
    res = db.execute("""SELECT category, weight, sub, main, competency_id, annual_appraisal_id, grade
	FROM public.competency;""")
    res = res.fetchall()
    return res

async def read_annual_appraisal(db:Session):
    res = db.execute("""SELECT * FROM public.annual_appraisal;""")
    res = res.fetchall()
    return res



async def create_end_of_year_review(assessment, score, weight, comment, appraisal_form_id, db: Session):
    res = db.execute("""INSERT INTO public.endofyear_review(assessment, score, comment, weight, appraisal_form_id)
    values(:assessment, :score, :comment, :appraisal_form_id, :annual_plan_id, :weight, :staff_id);""",
    {'assessment':assessment, 'score':score, 'comment':comment, 'weight':weight, 'appraisal_form_id':appraisal_form_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "end of year review has been created"})


# CREATE ANNUAL APPRAISAL FORM DETAILS 
# async def create_cc_organization_and_management(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "organization and management recorded"})

# async def create_cc_innovation_and_strategic_thinking(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "innovation and strategic thinking recorded"})    

# async def create_cc_leadership_and_decision_making(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "leadership and decision making recorded"})    

# async def create_cc_developing_and_improving(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "developing and improving recorded"})    

# async def create_cc_communication(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "communication recorded"})    

# async def create_cc_job_knowledge_and_technical_skills(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "job knowledge and technical skills recorded"})    

# async def create_cc_supporting_and_cooperating(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "supporting and cooperation recorded"})    

# async def create_cc_maximizing_and_maintaining_productivity(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "maximizing and maintaining productivity recorded"})    

# async def create_cc_developing_managingbudgets_and_savingcost(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "developing / managing and saving cost recorded"})    

# async def create_nc_ability_to_develop_staff(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "ability to develop staff recorded"})    

# async def create_nc_commitment_to_personal_development(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "commitment to personal development recorded"})    

# async def create_nc_delivering_results(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "delivering results and ensuring customer development recorded"})  

# async def create_nc_following_instructions(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "following instructions recorded"})  

# async def create_nc_respect_and_commitment(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "respect and commitment recorded"})  

# async def create_nc_ability_to_work_effectively_in_a_team(appraisal_form_id, weight, grade, comment, db:Session):
#     res = db.execute("""INSERT INTO public.competency(appraisal_form_id, weight, grade, comment)
#     values(:appraisal_form_id, :weight, :grade, :comment);""",
#     {'appraisal_form_id':appraisal_form_id, 'weight':weight, 'grade':grade, 'comment':comment})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "ability to work effectively in a team recorded"}) 

# CREATE ANNUAL APPRAISAL
async def create_annual_appraisal(payload: schemas.AnnualAppraisal, db:Session):
    query = db.execute(""" SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """) # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today(): # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN 
        res = db.execute("""INSERT INTO public.annual_appraisal(
	                    result_areas, target, resources, appraisal_form_id, submit)
	                    values(:result_areas, :target, :resources, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do 
	                    update set result_areas = EXCLUDED.result_areas, target = EXCLUDED.target, resources = EXCLUDED.resources, submit = EXCLUDED.submit; """,
                        {'appraisal_form_id':payload.appraisal_form_id, 'submit':payload.submit}) # CREATE INTO TABLE
        db.commit()
        if payload.submit==1:
            await email.start.approve_annual_plan(payload.appraisal_form_id) # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
        else:
            pass    
        
        return JSONResponse(status_code=200, content={"message": "annual plan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})





# async def update_end_of_year_review(end_of_year_review: schemas.update_end_of_year_review, db: Session):
#     res = db.execute("""UPDATE public.endofyear_review
# 	SET assessment = :assessment, score = :score, comment = :comment, appraisal_form_id = :appraisal_form_id, endofyear_review_id = :endofyear_review_id, annual_plan_id = :annual_plan_id, weight = :weight
# 	WHERE endofyear_review_id = :endofyear_review_id;""",
#     {'assessment':assessment, 'score':score, 'comment':comment, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id, 'endofyear_review_id':endofyear_review_id, 'weight':weight})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "end of year review has been updated"})

# async def update_core_competencies(core_competencies: schemas.update_core_competencies, db: Session):
#     res = db.execute("""UPDATE public.competency
# 	SET annual_appraisal_id = :annual_appraisal_id, competency_id = :competency_id, grade = :grade
# 	WHERE competency_id = :competency_id;""",
#     {'annual_appraisal_id':annual_appraisal_id, 'competency_id':competency_id, 'grade':grade})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "core competency has been updated"})

# async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
#     res = db.execute("""UPDATE public.annual_appraisal
# 	SET grade = comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
# 	WHERE annual_appraisal_id = :annual_appraisal_id;""",
#     {'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "annual appraisal has been updated"})


# async def delete_end_of_year_review(endofyear_review_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.endofyear_review
# 	WHERE endofyear_review_id = :endofyear_review_id;""",
#     {'endofyear_review_id':endofyear_review_id})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "end of year review has been deleted"})

# async def delete_core_competencies(competency_id: int, db:Session):
#     res = db.execute("""DELETE FROM public.competency
# 	WHERE competency_id = :competency_id;""",
#     {'competency_id': competency_id})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "core competency has been deleted"})

# async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.annual_appraisal
# 	WHERE annual_appraisal_id = :annual_appraisal_id;""",
#     {'annual_appraisal_id':annual_appraisal_id})
#     db.commit()
#     return JSONResponse(status_code=200, content={"message": "annual appraisal has been deleted"})
