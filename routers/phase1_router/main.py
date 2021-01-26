from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db



router = APIRouter()


@router.post("/create/{hash}")
async def create_phase1(payload:List[schemas.create_phase1], hash:str, db: Session = Depends(get_db)):
    return await crud.create_phase1(db, payload)

@router.delete("/delete/{id}")
async def delete_phase1(id: int, db: Session = Depends(get_db)):
    return await crud.delete_phase1(db, id)

@router.post("/check_email_hash")
async def check_email_hash(background_tasks:BackgroundTasks, db: Session = Depends(get_db)):
    return await crud.check_email_hash(db, background_tasks)

@router.post("/generate_email_hash")
async def generate_email_hash(db: Session = Depends(get_db)):
    return await crud.generate_email_hash(db)

@router.get("form/{hash}")
async def read_hash_form(hash: str, db: Session = Depends(get_db)):
    return await crud.read_hash_form(hash, db)

@router.get("/{id}")
async def read_phase_1_by_id(id:int, db: Session = Depends(get_db)):
    return await crud.read_phase_1_by_id(db,id)

@router.get("/")
async def read_phase_1(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    return await crud.read_phase_1(db,skip,limit,search,value)

@router.patch("/forms/{hash}")
async def update_hash_form(hash:str, payload: schemas.UpdateForm, db: Session = Depends(get_db)):
    return await crud.update_hash_form(hash,payload,db)

@router.patch("/{hash}")
async def update_phase_1_by_id(id: int, payload: schemas.UpdateForm, db: Session = Depends(get_db)):
    return await crud.update_phase_1_by_id(db,id,payload)

@router.post("/approve/{hash}")
async def approve_phase1(payload:List[schemas.approve_phase1], hash:str, db: Session = Depends(get_db)):
    return await crud.approve_phase1(payload,db)