from fastapi import HTTPException
from datetime import timedelta
from sqlalchemy.orm import Session
# import models
# import schemas
# import main
from . import models, schemas
import sys
import utils
from config import Settings as settings
import jwt

# GET USER BY ID

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sel@localhost:5432/farmerlynkz"
# SQLALCHEMY_DATABASE_URL = "postgresql://appraisal2:password@db:8434/appraisal"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()


async def read_user_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

# LOGIN USER


async def authenticate(payload: schemas.Auth, db: Session):
    try:
        user = db.query(models.User).filter(models.User.email ==
                                            payload.email).first()
        if not user:
            raise schemas.NotFoundError('user not found')
        user_type = db.execute(""" SELECT user_type_id FROM public.users where email=:email """, {
                               'email': payload.email})
        user_type = user_type.first()[0]
        if user_type < 3:
            # VERIFY PASSWORD
            if models.User.verify_hash(payload.password, user.password):
                # CREATE ACCESS TOKEN IF EMAIL AND PASSWORD ARE PRESENT
                access_token = utils.create_token(
                    data={'email': payload.email, 'id': user.id})
                refresh_token = utils.create_token(
                    data={'email': payload.email, 'id': user.id})
                return {"access_token": access_token, "refresh_token": refresh_token, "user": user}
            else:
                raise schemas.UnAuthorised('invalid password')
        else:
            raise schemas.UnAuthorised('user is not allowed to log in')
    except schemas.UnAuthorised:
        raise HTTPException(
            status_code=401, detail="{}".format(sys.exc_info()[1]))
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)


# LOG OUT USER
async def revoke_token(payload: schemas.Token, db: Session):
    try:
        db.add_all([models.RevokedToken(jti=token) for token in list(
            {v for (k, v) in payload.dict().items()}) if token is not None])
        db.commit()
        db.close()
        return True
    except schemas.ExpectationFailure:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)


# RELOAD USER
async def refresh_token(payload: schemas.Token, db: Session):
    try:
        if not payload.refresh_token:
            raise schemas.UnAcceptableError('refresh token needed')
        if await is_token_blacklisted(payload.refresh_token, db):
            raise schemas.UnAuthorised('refresh token blacklisted')
        if await revoke_token(payload, db):
            data = utils.decode_token(data=payload.refresh_token)
            access_token = utils.create_token(data={'email': data.get('email'), 'id': data.get(
                'id')}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_DURATION_IN_MINUTES))
            refresh_token = utils.create_token(data={'email': data.get('email'), 'id': data.get(
                'id')}, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES))
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            raise schemas.ExpectationFailure()
    except schemas.UnAcceptableError:
        raise HTTPException(
            status_code=422, detail="{}".format(sys.exc_info()[1]))
    except schemas.UnAuthorised:
        raise HTTPException(
            status_code=401, detail="{}".format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        raise HTTPException(
            status_code=417, detail="{}".format(sys.exc_info()[1]))
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=500, detail="{}".format(sys.exc_info()[1]))
    except schemas.NotFoundError:
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


# CHECK BLACKLISTED TOKEN
async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(
        models.RevokedToken.jti == token).first()  # GET EXPIRED TOKENS FROM DB
    if res is None:
        return False
    return True


# RESET PASSWORD
async def request_password_reset(payload: schemas.UserBase, db: Session, background_tasks):
    try:
        user = db.query(models.User).filter(models.User.email ==
                                            payload.email).first()  # CHECK IF USER IS PRESENT IN DB
        if not user:
            raise schemas.NotFoundError('user not found')
        while True:
            new_code = models.ResetPasswordCodes(
                user_id=user.id, code=models.ResetPasswordCodes.generate_code())
            code = db.query(models.ResetPasswordCodes).filter(
                models.ResetPasswordCodes.user_id == user.id).first()
            if code:
                db.delete(code)  # DELETE OLD CODE FROM DB
                db.flush()
            break
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        # scheduler.add_job(delete_password_reset_code, trigger='date', kwargs={'id': new_code.id},
        # id='ID{}'.format(new_code.id), replace_existing=True,
        # run_date=datetime.utcnow()+timedelta(minutes=settings.RESET_PASSWORD_SESSION_DURATION_IN_MINUTES))
        # # SEND NEW CODE TO THE USER IN MAIL
        # await send_in_background(background_tasks, Mail(email=['{}'.format(payload.email)],
        # content={'code':new_code.code}), reset_password_template)
        return True
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except schemas.UnAcceptableError:
        db.rollback()
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def request_password_reset_(payload: schemas.UserBase, db: Session, background_tasks):
    try:
        user = db.query(models.User).filter(models.User.email ==
                                            payload.email).first()  # CHECK IF USER IS PRESENT IN DB
        if not user:
            raise schemas.NotFoundError('user not found')
        while True:
            new_code = models.ResetPasswordCodes(
                user_email=user.email, code=models.ResetPasswordCodes.generate_code())
            code = db.query(models.ResetPasswordCodes).filter(
                models.ResetPasswordCodes.user_email == user.email).first()
            if code:
                db.delete(code)  # DELETE OLD CODE FROM DB
                db.flush()
            break
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        return True
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except schemas.UnAcceptableError:
        db.rollback()
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


# GET USERS LOGGED IN
async def get_current_user(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):  # CHECK IF TOKEN EXISTS
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(
            data=token, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # GET TOKEN DATA
        if token_data:
            # RETURN  DETAILS OF LOGGED IN USER
            return await read_user_by_id(token_data['id'], db)
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# DELETE PASSWORD RESET CODE
def delete_password_reset_code(id: int, db: Session = SessionLocal()):
    try:
        code = db.query(models.ResetPasswordCodes).filter(
            models.ResetPasswordCodes.id == id).first()
        if code:
            db.delete(code)
        db.commit()
        return True
    except schemas.UnAcceptableError:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
