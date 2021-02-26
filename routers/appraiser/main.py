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

@router.get("/completedlist/{user_id}/{deadline}")
async def read_completed_list(user_id:int, deadline:str, db: Session = Depends(get_db)):
    return await crud.read_completed_list(user_id, deadline, db)

@router.get("/incompletelist/{user_id}/{deadline}")
async def read_incomplete_list(user_id:int, deadline:str, db: Session = Depends(get_db)):
    return await crud.read_incomplete_list(user_id, deadline, db)

@router.get("/deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)

@router.post("/deadline/")
async def create_deadline(payload:schemas.create_deadline, db: Session = Depends(get_db) ):
    return await crud.create_deadline(payload.deadline_type, payload.start_date, payload.ending, db)

@router.put("/Deadline/")
async def update_deadline_table(deadline: schemas.update_deadline, db: Session = Depends(get_db)):
    return await crud.update_deadline(deadline, db)

@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    return await crud.delete_deadline(deadline_id, db)    
