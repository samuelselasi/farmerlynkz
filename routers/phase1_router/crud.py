from fastapi import Depends, HTTPException, BackgroundTasks
from services.email import background_send
from sqlalchemy.orm import Session
from . import models, schemas


async def create_appraisal_form(appraisal_form: schemas.create_appraisal_form, db:Session):
    res = db.execute("""INSERT INTO public.appraisal_form(department, grade, position, appraisal_form_id, date, staff_id) 
    VALUES (:department, :grade, :position, :appraisal_form_id, :date, :staff_id);""",
    {'department': appraisal_form.department, 'grade': appraisal_form.grade, 'position': appraisal_form.position, 'appraisal_form_id':appraisal_form.appraisal_form_id, 'date': appraisal_form.date, 'staff_id': appraisal_form.staff_id})
    db.commit()
    return res

async def read_appraisal_form(db:Session):
    res = db.execute("""SELECT department, grade, "position", appraisal_form_id, date, staff_id FROM public.appraisal_form;""")
    res = res.fetchall()
    return res

async def delete_appraisal_form(db:Session):
    res = db.execute("""DELETE FROM public.appraisal_form
	WHERE <condition>;""")
    db.commit()
    return res

async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session):
    res = db.execute("""UPDATE public.appraisal_form
	SET department=appraisal_form.department, grade=appraisal_form.grade, "position"=appraisal_form.position, appraisal_form_id=appraisal_form.appraisal_form_id, date=appraisal_form.date, staff_id=appraisal_form.staff_id
	WHERE appraisal_form_id=appraisal_form.appraisal_form_id;""")
    res = res.fetchall()
    return res

async def create_annual_plan(annual_plan: schemas.create_annual_plan, db:Session):
    res = db.execute("""INSERT INTO public.annual_plan(result_areas, target, resources, annual_plan_id, status, form_hash)
    VALUES (:result_areas, :target, :resources, :annual_plan_id, :status, :form_hash);""",{'result_areas':annual_plan.result_areas, 'target':annual_plan.target,'resources':annual_plan.resources, 'annual_plan_id': annual_plan.annual_plan_id,'status':annual_plan.status, 'form_hash':annual_plan.form_hash})
    db.commit()
    return res

async def read_annual_plan(db:Session):
    res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash FROM public.annual_plan;""")
    res = res.fetchall()
    return res

async def delete_annual_plan(db: Session):
    res = db.execute("""DELETE FROM public.annual_plan
	WHERE <condition>;""")
    db.commit()
    return res

async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session):
    res = db.execute("""UPDATE public.annual_plan
	SET result_areas=annual_plan.result_areas, target=annual_plan.target, resources=annual_plan.resources, appraisal_form_id=annual_plan.appraisal_form_id, annual_plan_id=annual_plan.annual_plan_id, status=annual_plan.status, form_hash=annual_plan.form_hash
	WHERE annual_plan_id=annual_plan.annual_plan_id;""")
    db.commit()
    return res

async def create_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db:Session):
    res = db.execute("""INSERT INTO public.annual_appraisal(grade, comment, field, appraisal_form_id, status, annual_appraisal_id) 
    VALUES (:grade, :comment, :field, :appraisal_form_id, :status, :annual_appraisal_id);""",
    {'grade':annual_appraisal.grade, 'comment':annual_appraisal.comment,'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'status':annual_appraisal.status, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
    db.commit()
    return res

async def read_annual_appraisal(db:Session):
    res = db.execute("""SELECT grade, comment, field, appraisal_form_id, status, annual_appraisal_id FROM public.annual_appraisal;""")
    res = res.fetchall()
    return res

async def delete_annual_appraisal(db: Session):
    res = db.execute("""DELETE FROM public.annual_appraisal
	WHERE <condition>;""")
    db.commit()
    return res

async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
    res = db.execute("""UPDATE public.annual_appraisal
	SET grade=annual_appraisal.grade, comment=annual_appraisal.comment, field=annual_appraisal.field, appraisal_form_id=annual_appraisal.appraisal_form_id, status=annual_appraisal.status, annual_appraisal_id=annual_appraisal.annual_appraisal_id
	WHERE annual_appraisal_id=annual_appraisal.annual_appraisal_id;""")
    db.commit()
    return res 

async def read_hash_form(hash_:str, db:Session):
    res = db.execute(""" SELECT public.get_hash_verification(:hash_) """,{'hash_':hash_})
    res = res.fetchall()
    return res

#/////////////////////////////////////////////////////////////
'''
async def create_review_start( db: Session, phase1: schemas.create_review_start ):
    for item in phase1:
        phase1 = models.phase1(kra=str(item.kra.dict()), target=str(item.target.dict()), resource_required=str(item.resource_required.dict()) )
        db.add(phase1)
    db.commit()
    return 'success'
    '''

async def delete_phase1(db: Session, id: int):
    phase1 = db.query(models.phase1).filter(models.phase1.id == id).first()
    if not phase1:
        return 'staff not found'
    db.delete(phase1)
    db.commit()
    return 'staff deleted'

async def generate_email_hash(db: Session, hash:str):
    pass

async def read_phase_1(db: Session, skip:int, limit:int, search:str, value:str):
    base = db.query(models.phase1)
    if search and value:
        try:
            base = base.filter(models.phase1.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_phase_1_by_id(db: Session, id: int):
    return db.query(models.phase1).filter(models.phase1.id == id).first()

async def update_hash_form(db: Session, hash:str):
    pass

async def  update_phase_1_by_id(db: Session, id: int):
    pass
    
# async def update_phase1(db:Session, id:int, phase1:schemas.update_phase1):
#     phase1 = await get_phase1_by_id(db, id)
#     if not phase1:
#         raise HTTPException(status_code=404)
#     updated = db.query(models.phase1).filter(models.phase1.id==id).update(phase1.dict(exclude_unset=True))
#     db.commit()
#     if updated:
#         return await get_phase1_by_id(db, id)