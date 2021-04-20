from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db, oauth2_scheme


router = APIRouter()


# GET PHASE-1 DETAILS
@router.get("/appraisalform/")
async def read_appraisal_form(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_appraisal_form_auth(token, db)

@router.get("/annualplan/")
async def read_annual_plan(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_annual_plan_auth(token, db)

@router.get("/annualappraisal/")
async def read_annual_appraisal(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_annual_appraisal_auth(token, db)

@router.get("/formdetails/{hash}/")
async def verify_hash_form(hash:str, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.verify_hash_form_auth(hash, token, db)

@router.get("/hashdetails/")
async def read_hash_form(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_hash_form_auth(token, db)

@router.get("/deadline/")
async def read_deadline_table(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_deadline_table_auth(token, db)


# CREATE PHASE-1 DETAILS
@router.post("/appraisalform/")
async def appraisal_form(payload:schemas.appraisal_form, db:Session=Depends(get_db)):
    return await crud.appraisal_form(payload.department, payload.grade, payload.positions, payload.date, payload.staff_id, db)

@router.post("/annualplan/")
async def create_annual_plan(payload:schemas.create_annual_plan, db:Session=Depends(get_db)):
    return await crud.create_annual_plan(payload.result_areas, payload.target, payload.resources, payload.appraisal_form_id, db)

@router.post("/createappraisalform/")
async def create_appraisal_form(payload:schemas.create_appraisal_form, db:Session=Depends(get_db)):
    return await crud.create_appraisal_form(payload.deadline, payload.department, payload.positions, payload.grade, payload.date, payload.staff_id, payload.progress_review, payload.remarks, payload.assessment, payload.score, payload.weight, payload.comment, db)

@router.post("/annualappraisal/")
async def create_annual_appraisal(payload:schemas.create_annual_appraisal, db:Session=Depends(get_db)):
    return await crud.create_annual_appraisal(payload.comment, payload.field, payload.appraisal_form_id, db)


# UPDATE PHASE-1 DETAILS
@router.put("/appraisalform/")
async def update_appraisal_form(appraisal_form:schemas.update_appraisal_form, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_appraisal_form_auth(appraisal_form, token, db)

@router.put("/annualplan/")
async def update_annual_plan(payload:schemas.update_annual_plan, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_annual_plan_auth(payload, token, db)

@router.put("/annualaprpaisal/")
async def update_annual_appraisal(annual_appraisal:schemas.update_annual_appraisal, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_annual_appraisal_auth(annual_appraisal, token, db)


# DELETE PHASE-1 DETAILS
@router.delete("/annualalan/{annual_plan_id}/")
async def delete_annual_plan(annual_plan_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_annual_plan_auth(annual_plan_id, token, db)

@router.delete("/appraisalform/{appraisal_form_id}/")
async def delete_appraisal_form(appraisal_form_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_appraisal_form_auth(appraisal_form_id, token, db)

@router.delete("/annualappraisal/{annual_appraisal_id}/")
async def delete_annual_appraisal(annual_appraisal_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_annual_appraisal_auth(annual_appraisal_id, token, db)



