from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()

@router.get("/midyearreview/")
async def read_mid_year_review(db: Session = Depends(get_db)):
    return await crud.read_mid_year_review(db)

# @router.get("/appraisalform/")
# async def read_appraisal_form(db: Session = Depends(get_db)):
#     return await crud.read_appraisal_form(db)

# @router.get("/annualplan/")
# async def read_annual_plan(db: Session = Depends(get_db)):
#     return await crud.read_annual_plan(db)

# @router.get("/annualappraisal/")
# async def read_annual_appraisal(db: Session = Depends(get_db)):
#     return await crud.read_annual_appraisal(db)

# @router.get("/formdetails/{hash}/")
# async def verify_hash_form(hash: str, db: Session = Depends(get_db)):
#     return await crud.verify_hash_form(hash, db)

# @router.get("/hashdetails/")
# async def read_hash_form(db: Session = Depends(get_db)):
#     return await crud.read_hash_form(db)


@router.post("/midyearreview/")
async def create_mid_year_review(payload: schemas.create_mid_year_review, db: Session = Depends(get_db)):
    return await crud.create_mid_year_review(payload.progress_review, payload.remarks, payload.mid_status, payload.appraisal_form_id, payload.annual_plan_id, db)

# @router.post("/appraisalform/")
# async def appraisal_form(payload: schemas.appraisal_form, db: Session = Depends(get_db)):
#     return await crud.appraisal_form(payload.department, payload.grade, payload.positions, payload.date, payload.staff_id, db)

# @router.post("/annualplan/")
# async def create_annual_plan(payload:schemas.create_annual_plan, db: Session = Depends(get_db)):
#     return await crud.create_annual_plan(payload.result_areas, payload.target, payload.resources, payload.appraisal_form_id, payload.form_hash, db)

# @router.post("/createappraisalform/")
# async def create_appraisal_form(payload: schemas.create_appraisal_form, db: Session = Depends(get_db)):
#     return await crud.create_appraisal_form(payload.department, payload.positions, payload.grade, payload.date, payload.staff_id, payload.progress_review, payload.remarks, payload.assessment, payload.score, payload.weight, payload.comment, db)

# @router.post("/annualappraisal/")
# async def create_annual_appraisal(payload:schemas.create_annual_appraisal, db: Session = Depends(get_db)):
#     return await crud.create_annual_appraisal(payload.grade, payload.comment, payload.field, payload.appraisal_form_id, db)

@router.put("/midyearreview/")
async def update_mid_year_review(mid_year_review: schemas.update_mid_year_review, db: Session = Depends(get_db)):
    return await crud.update_mid_year_review(mid_year_review, db)

# @router.put("/appraisalform/")
# async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session = Depends(get_db)):
#     return await crud.update_appraisal_form(appraisal_form, db)

# @router.put("/annualplan/")
# async def update_annual_plan(payload: schemas.update_annual_plan, db: Session = Depends(get_db)):
#     return await crud.update_annual_plan(payload, db)

# @router.put("/annualaprpaisal/")
# async def update_annual_appraisal(annual_appraisal: schemas.update_annual_appraisal, db: Session = Depends(get_db)):
#     return await crud.update_annual_appraisal(annual_appraisal, db)


@router.delete("/midyearreview/{midyear_review_id}/")
async def delete_mid_year_review(midyear_review_id: int, db: Session = Depends(get_db)):
    return await crud.delete_mid_year_review(midyear_review_id, db)

# @router.delete("/annualalan/{annual_plan_id}/")
# async def delete_annual_plan(annual_plan_id: int, db: Session = Depends(get_db)):
#     return await crud.delete_annual_plan(annual_plan_id, db)

# @router.delete("/appraisalform/{appraisal_form_id}/")
# async def delete_appraisal_form(appraisal_form_id:int, db: Session = Depends(get_db)):
#     return await crud.delete_appraisal_form(appraisal_form_id, db)

# @router.delete("/annualappraisal/{annual_appraisal_id}/")
# async def delete_annual_appraisal(annual_appraisal_id: int, db: Session = Depends(get_db)):
#     return await crud.delete_annual_appraisal(annual_appraisal_id, db)



# @router.post("/check_email_hash")
# def check_email_hash(background_tasks:BackgroundTasks):
#     return crud.check_email_hash(background_tasks)
