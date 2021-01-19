from fastapi import APIRouter, Depends, HTTPException

from pydantic import UUID4, EmailStr

from sqlalchemy.orm import Session

from typing import List, Optional

from . import crud, schemas

from main import get_db





router = APIRouter()



@router.get("/")
async def read_Phase1(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    return await crud.get_Phase1(db,skip,limit,search,value)



@router.get("/{id}")
async def read_phase1(db: Session = Depends(get_db)):
    return await crud.get_phase1(db,skip,limit)
     


@router.post("/create")
async def create_phase1(payload:List[schemas.create_phase1], db: Session = Depends(get_db)):
    return await crud.create_phase1(db, payload)



@router.delete("/delete/{id}")
async def delete_phase1(id: int, db: Session = Depends(get_db)):
    return await crud.delete_phase1(db, id)



@router.put("/update/{id}")
async def update_phase1(id: int, payload: schemas.update_phase1, db: Session = Depends(get_db)):
    return await crud.update_phase1(db,id,payload)
    


@router.post("/approve")
async def approve_phase1(payload:List[schemas.approve_phase1], db: Session = Depends(get_db)):
    return await crud.approve_phase1(payload,db)
