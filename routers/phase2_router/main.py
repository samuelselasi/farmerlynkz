from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()


# READ PHASE-2 DETAILS

@router.get("/midyearreview/")
async def read_mid_year_review(db: Session = Depends(get_db)):
    return await crud.read_mid_year_review(db)

@router.get("/appraisalform/")
async def read_appraisal_form(db:Session=Depends(get_db)):
    return await crud.read_appraisal_form(db)

@router.get("/annualplan/")
async def read_annual_plan(db:Session=Depends(get_db)):
    return await crud.read_annual_plan(db)

@router.get("/annualappraisal/")
async def read_annual_appraisal(db:Session=Depends(get_db)):
    return await crud.read_annual_appraisal(db)

@router.get("/formdetails/{hash}/")
async def verify_hash_form(hash:str, db:Session=Depends(get_db)):
    return await crud.verify_hash_form(hash, db)

@router.get("/hashdetails/")
async def read_hash_form(db:Session=Depends(get_db)):
    return await crud.read_hash_form(db)

@router.get("/deadline/")
async def read_deadline_table(db:Session=Depends(get_db)):
    return await crud.read_deadline_table(db)

# CREATE PHASE-2 DETAILS

@router.post("/midyearreview/")
async def create_mid_year_review(payload: schemas.create_mid_year_review, db: Session = Depends(get_db)):
    return await crud.create_mid_year_review(payload.progress_review, payload.remarks, payload.mid_status, payload.appraisal_form_id, payload.annual_plan_id, db)


# UPDATE PHASE-2 DETAILS

@router.put("/midyearreview/")
async def update_mid_year_review(mid_year_review: schemas.update_mid_year_review, db: Session = Depends(get_db)):
    return await crud.update_mid_year_review(mid_year_review, db)


# DELETE PHASE-2 DETAILS

@router.delete("/midyearreview/{midyear_review_id}/")
async def delete_mid_year_review(midyear_review_id: int, db: Session = Depends(get_db)):
    return await crud.delete_mid_year_review(midyear_review_id, db)
