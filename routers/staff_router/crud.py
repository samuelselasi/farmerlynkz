from sqlalchemy.orm import Session

from . import models, schemas

from fastapi import Depends






async def create_staff( db: Session, staff: schemas.staff ):
    staff = models.staff(title=staff.title, description=staff.description)
    db.add(staff)
    db.commit()
    return 'success'


    
async def get_Staff(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    base = db.query(models.staff)
    if search and value:
        try:
            base = base.filter(models.staff.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()



async def get_staff(db: Session, id: int):
    return db.query(models.staff).filter(models.staff.id == id).first()



async def delete_staff(db: Session, id: int):
    staff = db.query(models.staff).filter(models.staff.id == id).first()
    if not staff:
        return 'staff not found'
    db.delete(staff)
    db.commit()
    return 'staff deleted'



async def update_staff(db: Session, id: int, payload: schemas.staffCreate):
    staff = db.query(models.staff).filter(models.staff.id == id).first()
    if not staff:
        return 'staff not found'
    res = db.query(models.staff).filter(models.staff.id == id).update(payload)
    db.commit()
    return res


