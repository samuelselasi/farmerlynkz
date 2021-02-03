from fastapi import APIRouter, Depends, HTTPException

from pydantic import UUID4, EmailStr

from sqlalchemy.orm import Session

from typing import List, Optional

from . import crud, schemas

from main import get_db





router = APIRouter()


@router.get("/{user_id}")
async def read_appraiser_appraisees(user_id:int, db: Session = Depends(get_db)):
    return await crud.read_appraiser_appraisees(user_id, db)
    # return await crud.read_appraiser_appraisees(db,skip,limit,search,value)