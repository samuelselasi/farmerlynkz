from fastapi import Depends, HTTPException, BackgroundTasks
from services.email import background_send
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


# async def read_annual_plan(db:Session):
#     res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash FROM public.annual_plan;""")
#     res = res.fetchall()
#     return res

# async def read_annual_appraisal(db:Session):
#     res = db.execute("""SELECT grade, comment, field, appraisal_form_id, status, annual_appraisal_id FROM public.annual_appraisal;""")
#     res = res.fetchall()
#     return res

# async def verify_hash_form(hash_:str, db:Session):
#     res = db.execute(""" SELECT public.get_hash_verification(:hash_) """,{'hash_':hash_})
#     res = res.fetchall()
#     return res

# async def read_hash_form(db:Session):
#     res = db.execute("""SELECT hash, email, hash_table_id
# 	FROM public.hash_table;""")
#     res = res.fetchall()
#     return res


async def create_end_of_year_review(assessment, score, comment, appraisal_form_id, annual_plan_id, weight, staff_id, db: Session):
    res = db.execute("""INSERT INTO public.endofyear_review(assessment, score, comment, appraisal_form_id, annual_plan_id, weight)
    values(:assessment, :score, :comment, :appraisal_form_id, :annual_plan_id, :weight, :staff_id);""",
    {'assessment':assessment, 'score':score, 'comment':comment, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id, 'weight':weight})
    db.commit()
    return res

async def create_core_competencies(annual_appraisal_id, grade, db:Session):
    res = db.execute("""INSERT INTO public.competency(annual_appraisal_id, grade)
    values(:annual_appraisal_id, :grade);""",
    {'annual_appraisal_id':grade, 'grade':grade})
    db.commit()
    return res

async def create_annual_appraisal(comment, field, appraisal_form_id, db:Session):
    res = db.execute("""insert into public.annual_appraisal(comment, field, appraisal_form_id)
    values(:comment, :field, :appraisal_form_id);""",
    {'comment':comment,'field':field, 'appraisal_form_id':appraisal_form_id})
    db.commit()
    return res

# async def appraisal_form(department, grade, positions, date, staff_id, db:Session):
#     res = db.execute("""insert into public.appraisal_form(department, grade, positions, date, staff_id)
#     values(:department, :grade, :positions, :date, :staff_id);""",
#     {'department':department, 'grade':grade, 'positions':positions, 'date':date, 'staff_id':staff_id})
#     db.commit()
#     return res

# async def create_annual_plan(result_areas, target, resources, appraisal_form_id, form_hash, dfb:Session):
#     res = db.execute("""insert into public.annual_plan(result_areas, target, resources, appraisal_form_id, form_hash)
#     values(:result_areas, :target, :resources, :appraisal_form_id, :form_hash);""",
#     {'result_areas':result_areas, 'target':target,'resources':resources, 'appraisal_form_id':appraisal_form_id, 'form_hash':form_hash})
#     db.commit()
#     return res

# async def create_annual_appraisal(grade, comment, field, appraisal_form_id, db:Session):
#     res = db.execute("""insert into public.annual_appraisal(grade, comment, field, appraisal_form_id)
#     values(:grade, :comment, :field, :appraisal_form_id);""",
#     {'grade':grade, 'comment':comment,'field':field, 'appraisal_form_id':appraisal_form_id})
#     db.commit()
#     return res


async def update_end_of_year_review(end_of_year_review: schemas.update_end_of_year_review, db: Session):
    res = db.execute("""UPDATE public.endofyear_review
	SET assessment = :assessment, score = :score, comment = :comment, appraisal_form_id = :appraisal_form_id, endofyear_review_id = :endofyear_review_id, annual_plan_id = :annual_plan_id, weight = :weight
	WHERE endofyear_review_id = :endofyear_review_id;""",
    {'assessment':assessment, 'score':score, 'comment':comment, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id, 'endofyear_review_id':endofyear_review_id, 'weight':weight})
    db.commit()
    return res

async def update_core_competencies(core_competencies: schemas.update_core_competencies, db: Session):
    res = db.execute("""UPDATE public.competency
	SET annual_appraisal_id = :annual_appraisal_id, competency_id = :competency_id, grade = :grade
	WHERE competency_id = :competency_id;""",
    {'annual_appraisal_id':annual_appraisal_id, 'competency_id':competency_id, 'grade':grade})
    db.commit()
    return res

async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
    res = db.execute("""UPDATE public.annual_appraisal
	SET grade = comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
    db.commit()
    return res 

# async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session):
#     res = db.execute("""UPDATE public.annual_plan 
#     SET result_areas = :result_areas, target = :target, resources = :resources, annual_plan_id = :annual_plan_id, status = :status, form_hash = :form_hash
# 	WHERE annual_plan_id = :annual_plan_id;""", 
#     {'result_areas':annual_plan.result_areas, 'target':annual_plan.target,'resources':annual_plan.resources, 'annual_plan_id':annual_plan.annual_plan_id, 'status':annual_plan.status, 'form_hash':annual_plan.form_hash})
#     db.commit()
#     return res

# async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
#     res = db.execute("""UPDATE public.annual_appraisal
# 	SET grade = :grade, comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
# 	WHERE annual_appraisal_id = :annual_appraisal_id;""",
#     {'grade':annual_appraisal.grade, 'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
#     db.commit()
#     return res 


async def delete_end_of_year_review(endofyear_review_id: int, db: Session):
    res = db.execute("""DELETE FROM public.endofyear_review
	WHERE endofyear_review_id = :endofyear_review_id;""",
    {'endofyear_review_id':endofyear_review_id})
    db.commit()
    return res

async def delete_core_competencies(competency_id: int, db:Session):
    res = db.execute("""DELETE FROM public.competency
	WHERE competency_id = :competency_id;""",
    {'competency_id': competency_id})
    db.commit()
    return res

async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_appraisal
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
    {'annual_appraisal_id':annual_appraisal_id})
    db.commit()
    return res

# async def delete_annual_plan(annual_plan_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.annual_plan
# 	WHERE annual_plan_id = :annual_plan_id;""",
#     {'annual_plan_id': annual_plan.annual_plan_id})
#     db.commit()
#     return res

# async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.annual_appraisal
# 	WHERE annual_appraisal_id = :annual_appraisal.annual_appraisal_id;""",
#     {'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
#     db.commit()
#     return res



# async def create_review_start( db: Session, phase1: schemas.create_review_start ):
#     for item in phase1:
#         phase1 = models.phase1(kra=str(item.kra.dict()), target=str(item.target.dict()), resource_required=str(item.resource_required.dict()) )
#         db.add(phase1)
#     db.commit()
#     return 'success'
    
# async def read_phase_1(db: Session, skip:int, limit:int, search:str, value:str):
#     base = db.query(models.phase1)
#     if search and value:
#         try:
#             base = base.filter(models.phase1.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def update_hash_form(db: Session, hash:str):
#     pass