from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()


@router.post("/annual_plan")
async def create_annual_plan(payload:schemas.create_annual_plan, db: Session = Depends(get_db)):
    return await crud.create_annual_plan(payload.result_areas, payload.target, payload.resources, payload.appraisal_form_id, payload.form_hash, db)

@router.get("/")
async def read_annual_plan(db: Session = Depends(get_db)):
    return await crud.read_annual_plan(db)

@router.delete("/annual/plan")
async def delete_annual_plan(annual_plan: schemas.delete_annual_plan, db: Session = Depends(get_db)):
    return await crud.delete_annual_plan(annual_plan, db)

@router.put("/annual/plan")
async def update_annual_plan(payload: schemas.update_annual_plan, db: Session = Depends(get_db)):
    return await crud.update_annual_plan(payload, db)

@router.post("/appraisal/form")
async def appraisal_form(payload: schemas.appraisal_form, db: Session = Depends(get_db)):
    return await crud.appraisal_form(payload.department, payload.grade, payload.position, payload.date, payload.staff_id, db)

@router.post("/create/appraisal/form/")
async def create_appraisal_form(payload: schemas.create_appraisal_form, db: Session = Depends(get_db)):
    return await crud.create_appraisal_form(payload.department, payload.position, payload.grade, payload.date, payload.staff_id, payload.progress_review, payload.remarks, payload.assessment, payload.score, payload.weight, payload.comment, db)

@router.get("/appraisal/form")
async def read_appraisal_form(db: Session = Depends(get_db)):
    return await crud.read_appraisal_form(db)

@router.delete("/appraisal/form")
async def delete_appraisal_form(appraisal_form:schemas.delete_appraisal_form, db: Session = Depends(get_db)):
    return await crud.delete_appraisal_form(appraisal_form, db)

@router.put("/appraisal/form")
async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session = Depends(get_db)):
    return await crud.update_appraisal_form(appraisal_form, db)

@router.post("/annual_appraisal")
async def create_annual_appraisal(payload:schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(payload.grade, payload.comment, payload.field, payload.appraisal_form_id, db)

@router.get("/annual/appraisal")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)

@router.delete("/annual/appraisal")
async def delete_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.delete_annual_appraisal(db)

@router.put("/annual/aprpaisal")
async def update_annual_appraisal(annual_appraisal_id: int, db: Session = Depends(get_db)):
    return await crud.update_annual_appraisal(annual_appraisal_id, db)

@router.delete("/annual/appraisal/")
async def delete_annual_appraisal(annual_appraisal:schemas.delete_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.delete_annual_appraisal(annual_appraisal, db)

@router.get("/form/{hash}")
async def read_hash_form(hash: str, db: Session = Depends(get_db)):
    return await crud.read_hash_form(hash, db)
  
# @router.post("/check_email_hash")
# def check_email_hash(background_tasks:BackgroundTasks):
#     return crud.check_email_hash(background_tasks)
