from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db
from datetime import datetime

router = APIRouter()


@router.get("/competencedetails/")
async def read_competence_details(db: Session = Depends(get_db)):
    return await crud.read_competence_details(db)


@router.get("/performancedetails/")
async def read_cperformance_details(db: Session = Depends(get_db)):
    return await crud.read_performance_details(db)


@router.get("/annualappraisal/")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)


@router.post("/annualappraisal/")
async def create_annual_appraisal(payload: schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(payload, db)


@router.post("/competencedetails/")
async def create_competence_details(competence_id: int, grade: int, submit: int, appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.competence_details(competence_id, grade, submit, appraisal_form_id, db)


@router.post("/performancedetails/")
async def create_performance_details(assessment: int, final_score: int, weight: int, comment: str, submit: int,  approval_date: datetime, appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.performance_details(assessment, final_score, weight, comment, submit,  approval_date, appraisal_form_id, db)
