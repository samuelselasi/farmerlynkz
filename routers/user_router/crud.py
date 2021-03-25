from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from fastapi import Depends, HTTPException
from ..auth_router.models import ResetPasswordCodes
from exceptions import NotFoundError, UnAcceptableError, ExpectationFailure
from sqlalchemy.orm import Session
from . import models, schemas
from main import get_db
import sqlalchemy
import utils
import sys

async def create_user(payload:schemas.UserCreate, db:Session=Depends(get_db)):    
    try:  
        if not db.query(models.UserType).filter(models.UserType.id==payload.user_type_id).first():
            raise NotFoundError('user type not found')
        new_user = models.User(**payload.dict(exclude={'first_name','middle_name','last_name','password'}), password=models.User.generate_hash(payload.password))
        db.add(new_user)
        user_info = models.UserInfo(**payload.dict(exclude={'email','password','user_type_id','status'}),user=new_user)
        db.add(user_info) 
        db.commit()
        db.refresh(new_user) 
        return new_user
    except NotFoundError:
        raise HTTPException(status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def read_users(db:Session=Depends(get_db), skip:int=0, limit:int=100, search:str=None, value:str=None):
    try:
        base = db.query(models.User)
        if search and value:
            try:
                base = base.filter(models.User.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)
        
async def read_user_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == id).first()

async def delete_user(id: int, db):
    try:
        user = await read_user_by_id(id, db)
        if user:
            db.delete(user)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def update_user(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        if not await read_user_by_id(id, db):
            raise NotFoundError('user not found')
        res = db.query(models.UserInfo).filter(models.UserInfo.user_id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        if bool(res):
            return await read_user_by_id(id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def verify_password(id, payload: schemas.ResetPassword, db: Session):
    try:
        user = await read_user_by_id(id,db)
        if not user:
            raise NotFoundError("user with id: {} was not found".format(id))
        return models.User.verify_hash(payload.password, user.password)
    except NotFoundError:
        raise HTTPException(status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except:
        raise HTTPException(status_code=500, detail='{}'.format(sys.exc_info()[1]))

async def reset_password(id, payload: schemas.ResetPassword, db: Session):
    try:
        if not payload.code:
            raise UnAcceptableError('code required')
        if not await read_user_by_id(id,db):
            raise NotFoundError('user not found')
        if not await verify_code(id, payload.code, db):
            raise ExpectationFailure('could not verify reset code')
        res = db.query(models.User).filter(models.User.id == id).update({'password':models.User.generate_hash(payload.password)})
        db.commit()
        return True
    except UnAcceptableError:
        raise HTTPException(status_code=422, detail='{}'.format(sys.exc_info()[1]))
    except NotFoundError:
        raise HTTPException(status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(status_code=417, detail='{}'.format(sys.exc_info()[1]))
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def verify_code(id, code, db: Session):
    return db.query(ResetPasswordCodes).filter(sqlalchemy.and_(ResetPasswordCodes.user_id == id, ResetPasswordCodes.code == code)).first()
