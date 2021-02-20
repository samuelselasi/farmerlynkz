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