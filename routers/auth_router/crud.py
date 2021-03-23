from exceptions import NotFoundError, UnAuthorised, UnAcceptableError, ExpectationFailure
# from services.email import send_in_background, Mail
# from static.email_templates.reset_password import reset_password_template
from ..user_router.crud import read_user_by_id
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from main import settings
from sqlalchemy.orm import Session
from database import SessionLocal
from . import models, schemas
import sys, utils, jwt

async def authenticate(payload: schemas.Auth, db: Session):
    try:
        user = db.query(models.User).filter(models.User.email==payload.email).first()
        if not user:
            raise NotFoundError('user not found')
        if models.User.verify_hash(payload.password, user.password):
            access_token = utils.create_token(data = {'email':payload.email,'id':user.id})
            refresh_token = utils.create_token(data = {'email':payload.email,'id':user.id})
            return {"access_token": access_token.decode("utf-8"), "refresh_token": refresh_token.decode("utf-8"), "user": user}
        else:
            raise UnAuthorised('invalid password')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]))
    except NotFoundError:
        raise HTTPException(status_code=404, detail="{}".format(sys.exc_info()[1]))
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def revoke_token(payload: schemas.Token, db: Session):
    try:
        db.add_all([models.RevokedToken(jti=token) for token in list({v for (k,v) in payload.dict().items()}) if token is not None])
        db.commit()
        db.close() 
        return True
    except:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def refresh_token(payload: schemas.Token, db: Session):
    try:
        if not payload.refresh_token:
            raise UnAcceptableError('refresh token needed')
        if await is_token_blacklisted(payload.refresh_token, db):
            raise UnAuthorised('refresh token blacklisted')
        if await revoke_token(payload, db):
            data = utils.decode_token(data=payload.refresh_token) 
            access_token = utils.create_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_DURATION_IN_MINUTES))
            refresh_token = utils.create_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES))
            return {'access_token': access_token.decode("utf-8"), 'refresh_token': refresh_token.decode("utf-8")}
        else:
            raise ExpectationFailure()
    except UnAcceptableError:
        raise HTTPException(status_code=422, detail="{}".format(sys.exc_info()[1]))
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(status_code=417, detail="{}".format(sys.exc_info()[1]))
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()[1]))
    except:
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)
  
async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti == token).first()
    if res is None:
        return False
    return True

async def request_password_reset(payload: schemas.UserBase, db: Session, background_tasks):
    try:
        user = db.query(models.User).filter(models.User.email==payload.email).first()
        if not user:
            raise NotFoundError('user not found')
        while True:
            new_code = models.ResetPasswordCodes(user_id=user.id, code=models.ResetPasswordCodes.generate_code())
            code = db.query(models.ResetPasswordCodes).filter(models.ResetPasswordCodes.user_id==user.id).first()
            if code:
                db.delete(code)
                db.flush()
            break
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        # scheduler.add_job(delete_password_reset_code, trigger='date', kwargs={'id': new_code.id}, id='ID{}'.format(new_code.id), replace_existing=True, run_date=datetime.utcnow()+timedelta(minutes=settings.RESET_PASSWORD_SESSION_DURATION_IN_MINUTES))
        # await send_in_background(background_tasks, Mail(email=['{}'.format(payload.email)], content={'code':new_code.code}), reset_password_template)
        return True
    except NotFoundError:
        raise HTTPException(status_code=404, detail="{}".format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(status_code=404, detail="{}".format(sys.exc_info()[1]))
    except:
        db.rollback()
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def get_current_user(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_user_by_id(token_data['id'], db)
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

def delete_password_reset_code(id: int, db: Session = SessionLocal()):
    try:
        code = db.query(models.ResetPasswordCodes).filter(models.ResetPasswordCodes.id==id).first()
        if code:
            db.delete(code)
        db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)