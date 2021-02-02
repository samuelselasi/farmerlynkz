from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()


@router.post("/annual_plan")
async def create_annual_plan(create_annual_plan:schemas.create_annual_plan, db: Session = Depends(get_db)):
    return await crud.create_annual_plan(create_annual_plan, db)

@router.get("/")
async def read_annual_plan(db: Session = Depends(get_db)):
    return await crud.read_annual_plan(db)

@router.delete("/annual/plan")
async def delete_annual_plan(db: Session = Depends(get_db)):
    return await crud.delete_annual_plan(db)

@router.put("annual/plan")
async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session = Depends(get_db)):
    return await crud.update_annual_plan(annual_plan, db)

@router.post("/appraisal/form")
async def create_appraisal_form(appraisal_form:schemas.create_appraisal_form, db: Session = Depends(get_db)):
    return await crud.create_appraisal_form(appraisal_form, db)

@router.get("/appraisal/form")
async def read_appraisal_form(db: Session = Depends(get_db)):
    return await crud.read_appraisal_form(db)

@router.delete("/appraisal/form")
async def delete_appraisal_form(db: Session = Depends(get_db)):
    return await crud.delete_appraisal_form(db)

@router.put("/appraisal/form")
async def update_appraisal_form(db: Session = Depends(get_db)):
    return await crud.update_appraisal_form(db)

@router.post("/annual_appraisal")
async def create_annual_appraisal(create_annual_appraisal:schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(create_annual_appraisal, db)

@router.get("/annual/appraisal")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)

@router.delete("/annual/appraisal")
async def delete_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.delete_annual_appraisal(db)

@router.put("/annual/aprpaisal")
async def update_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.update_annual_appraisal(db)

# @router.post("/check_email_hash")
# def check_email_hash(background_tasks:BackgroundTasks):
#     return crud.check_email_hash(background_tasks)

@router.get("form/{hash}")
async def read_hash_form(hash: str, db: Session = Depends(get_db)):
    return await crud.read_hash_form(hash, db)