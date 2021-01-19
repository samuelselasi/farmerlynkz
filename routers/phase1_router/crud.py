from sqlalchemy.orm import Session

from fastapi import Depends

from . import models, schemas




async def create_phase1( db: Session, phase1: schemas.create_phase1 ):
    for item in phase1:
        phase1 = models.phase1(kra=str(item.kra.dict()), target=str(item.target.dict()), resource_required=str(item.resource_required.dict()) )
        db.add(phase1)
    db.commit()
    return 'success'

async def update_phase1(db:Session, id:int, phase1:schemas.update_phase1):
    phase1 = await get_phase1_by_id(db, id)
    if not phase1:
        raise HTTPException(status_code=404)
    updated = db.query(models.phase1).filter(models.phase1.id==id).update(phase1.dict(exclude_unset=True))
    db.commit()
    if updated:
        return await get_phase1_by_id(db, id)
    
async def get_Phase1(db: Session, skip:int, limit:int, search:str, value:str):
    base = db.query(models.phase1)
    if search and value:
        try:
            base = base.filter(models.phase1.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()



async def get_phase1_by_id(db: Session, id: int):
    return db.query(models.phase1).filter(models.phase1.id == id).first()



async def delete_phase1(db: Session, id: int):
    phase1 = db.query(models.phase1).filter(models.phase1.id == id).first()
    if not phase1:
        return 'staff not found'
    db.delete(phase1)
    db.commit()
    return 'staff deleted'



# async def update_phase1(db: Session, id: int, payload: schemas.create_phase1):
#     phase1 = db.query(models.phase1).filter(models.phase1.id == id).first()
#     if not phase1:
#         return 'staff not found'
#     res = db.query(models.phase1).filter(models.phase1.id == id).update(payload)
#     db.commit()
#     return res



async def approve_phase1( db: Session, phase1: schemas.approve_phase1 ):
    phase1 = models.phase1(id= int, kra=phase1.kra, target=phase1.target, resource_required=phase1.resource_required)
    db.add(phase1)
    db.commit()
    return 'success'

