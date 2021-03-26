from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()


@router.get("/Appraisees/{user_id}/")
async def read_appraiser_appraisees(user_id:int, db: Session = Depends(get_db)):
    return await crud.read_appraiser_appraisees(user_id, db)

@router.get("/completedlist/start/")
async def read_completed_list(deadline = 'Start', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_completed_list( deadline, user_id, db)

@router.get("/approved/start/")
async def read_approved_forms(deadline = 'Start', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_approved_forms( deadline, user_id, db)

@router.get("/approved/mid/")
async def read_approved_forms(deadline = 'Mid', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_approved_forms( deadline, user_id, db)

@router.get("/approved/end/")
async def read_approved_forms(deadline = 'End', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_approved_forms( deadline, user_id, db)

@router.get("/completedlist/mid/")
async def read_completed_list(deadline = 'Mid', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_completed_list( deadline, user_id, db)

@router.get("/completedlist/end/")
async def read_completed_list(deadline = 'End', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_completed_list( deadline, user_id, db)

@router.get("/waitingapproval/start/")
async def waiting_approval_list(deadline = 'Start', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.waiting_approval_list( deadline, user_id, db)

@router.get("/waitingapproval/mid/")
async def waiting_approval_list(deadline = 'Mid', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.waiting_approval_list( deadline, user_id, db)

@router.get("/waitingapproval/end/")
async def waiting_approval_list(deadline = 'End', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.waiting_approval_list( deadline, user_id, db)

@router.get("/incompletedlist/start/")
async def read_incompleted_list(deadline = 'Start', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_incomplete_list( deadline, user_id, db)   

@router.get("/incompletedlist/mid/")
async def read_incompleted_list(deadline = 'Mid', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_incomplete_list( deadline, user_id, db)  

@router.get("/incompletedlist/end/")
async def read_incompleted_list(deadline = 'End', user_id = 1,  db: Session = Depends(get_db)):
    return await crud.read_incomplete_list( deadline, user_id, db)  

@router.get("/deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)

@router.get("/deadline/start/")
async def read_start_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_start_deadline_table(db)

@router.get("/deadline/mid/")
async def read_mid_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_mid_deadline_table(db)

@router.get("/deadline/end/")
async def read_end_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_end_deadline_table(db)

@router.get("/supervisors/")
async def read_supervisors(db: Session = Depends(get_db)):
    return await crud.read_supervisors(db)

@router.get("/yearlyformdetails/{staff_id}/{form_year}")
async def read_yearly_form_deatails(staff_id:int, form_year:int, db: Session = Depends(get_db)):
    return await crud.read_yearly_form_deatails(staff_id, form_year, db)

@router.get("/approveform/{appraisal_form_id}/")
async def approve_form(appraisal_form_id:int, type_form='Start', db: Session = Depends(get_db)):
    return await crud.approve_form(appraisal_form_id, type_form, db)


@router.post("/deadline/")
async def create_deadline(payload:schemas.create_deadline, db: Session = Depends(get_db) ):
    return await crud.create_deadline(payload.deadline_type, payload.start_date, payload.ending, db)



@router.put("/Deadline/")
async def update_deadline_table(deadline: schemas.update_deadline, db: Session = Depends(get_db)):
    return await crud.update_deadline(deadline, db)



@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    return await crud.delete_deadline(deadline_id, db)    
