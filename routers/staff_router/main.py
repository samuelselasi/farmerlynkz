from fastapi import APIRouter, Depends, HTTPException

from pydantic import UUID4, EmailStr

from sqlalchemy.orm import Session

from typing import List, Optional

from main import get_db





router = APIRouter()



# @router.get("/all")
# async def read_Staff(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None,):
#     return await crud.get_Staff(db,skip,limit,search,value)



# @router.get("/{id}")
# async def read_staff(id: int, db: Session = Depends(get_db)):
#     return await crud.get_staff(db, id)
     


# @router.post("/create")
# async def create_staff(staff:schemas.staffCreate, db: Session = Depends(get_db)):
#     return await crud.create_staff(db, staff)



# @router.delete("/delete/{id}")
# async def delete_staff(id: int, db: Session = Depends(get_db)):
#     return await crud.delete_staff(db, id)



# @router.put("/update/{id}")
# async def update_staff(id: int, payload: schemas.staffCreate, db: Session = Depends(get_db)):
#     return await crud.update_staff(db,id,payload)

