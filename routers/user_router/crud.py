from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
# import models
# import schemas
# import main
import sqlalchemy
import utils
import jwt
import sys
from config import Settings as settings


async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti ==
                                               token).first()  # GET EXPIRED TOKENS FROM DB
    if res is None:
        return False
    return True


# GET USERS
async def read_users(db: Session, skip: int = 0, limit: int = 100,
                     search: str = None, value: str = None):
    try:
        base = db.query(models.User)  # GET USERS FROM DB
        if search and value:
            try:
                base = base.filter(
                    models.User.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except KeyError:
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def read_users_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(
            data=token, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if token_data:
            return await read_users(db)
        else:
            return schemas.nAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# GET USER BY ID
async def read_user_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()


async def read_user_by_id_auth(id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(
            data=token, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if token_data:
            return await read_user_by_id(id, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# GET USER BY EMAIL
async def read_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def read_user_by_email_auth(email: str, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(
            data=token, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if token_data:
            return await read_user_by_email(email, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})

# CREATE USER


async def create_user(payload: schemas.UserCreate, db: Session):
    try:
        if not db.query(models.UserType).filter(models.UserType.id == payload.user_type_id).first():
            raise schemas.NotFoundError('user type not found')
        new_user = models.User(
            **payload.dict(exclude={'password'}),
            password=models.User.generate_hash(payload.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=409)
    except KeyError:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def create_user_auth(payload: schemas.UserCreate, token: str,
                           db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await create_user(payload, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# PASSWORD VERIFICATION
async def verify_password(id, payload: schemas.ResetPassword, db: Session):
    try:
        user = await read_user_by_id(id, db)
        if not user:
            raise schemas.NotFoundError(
                "user with id: {} was not found".format(id))
        return models.User.verify_hash(payload.password, user.password)
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except schemas.UnAuthorised:
        raise HTTPException(
            status_code=500, detail='{}'.format(sys.exc_info()[1]))


async def verify_password_auth(id, payload: schemas.ResetPassword,
                               token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_password(id, payload, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ HASH DETAILS
async def read_hash_code(code: str, db: Session):
    res = db.execute(
        """SELECT id, code, user_id, user_email, status, date_created, date_modified
            FROM public.reset_password_codes where code=:code""", {'code': code})
    res = res.fetchall()
    return res

# READ HASH TABLE


async def read_hash_table(db: Session):
    res = db.execute(
        """ SELECT id, code, user_id, user_email, status, date_created, date_modified
         FROM public.reset_password_codes; """)
    res = res.fetchall()
    return res


# RESET PASSWORD BY ID
async def reset_password(id, payload: schemas.ResetPassword, db: Session):
    try:
        if not payload.code:
            raise schemas.UnAcceptableError('code required')
        if not await read_user_by_id(id, db):
            raise schemas.NotFoundError('user not found')
        if not await verify_code(id, payload.code, db):
            raise schemas.ExpectationFailure('could not verify reset code')
        db.query(models.User).filter(models.User.id == id).update(
            {'password': models.User.generate_hash(payload.password)})
        db.commit()
        return True
    except schemas.UnAcceptableError:
        raise HTTPException(
            status_code=422, detail='{}'.format(sys.exc_info()[1]))
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        raise HTTPException(
            status_code=417, detail='{}'.format(sys.exc_info()[1]))
    except schemas.UnAuthorised:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def verify_code_(email, code, db: Session):
    return db.query(models.ResetPasswordCodes).filter(
        sqlalchemy.and_(models.ResetPasswordCodes.user_email == email,
                        models.ResetPasswordCodes.code == code)).first()


async def verify_code_auth_(email, code, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_code_(email, code, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


async def reset_password_auth(id, payload: schemas.ResetPassword,
                              token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await reset_password(id, payload, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})

# RESET PASSWORD BY EMAIL


async def reset_password_(email, payload: schemas.ResetPassword, db: Session):
    try:
        if not payload.code:
            raise schemas.UnAcceptableError('code required')
        if not await read_user_by_email(email, db):
            raise schemas.NotFoundError('user not found')
        if not await verify_code_(email, payload.code, db):
            raise schemas.ExpectationFailure('could not verify reset code')
        db.query(models.User).filter(models.User.email == email).update(
            {'password': models.User.generate_hash(payload.password)})
        db.commit()
        return True
    except schemas.UnAcceptableError:
        raise HTTPException(
            status_code=422, detail='{}'.format(sys.exc_info()[1]))
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except schemas.ExpectationFailure:
        raise HTTPException(
            status_code=417, detail='{}'.format(sys.exc_info()[1]))
    except schemas.UnAuthorised:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def reset_password_auth_(email, payload: schemas.ResetPassword,
                               token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await reset_password_(email, payload, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})

# CHANGE PASSWORD


# CHANGE PASSWORD BY EMAIL(IN USE TO RESET PASSWORD)
async def change_password(email: str, password: str, db: Session):
    db.execute(""" UPDATE public.users SET email=:email, password=:password WHERE email=:email; """,
               {
                   'email': email, 'password': models.User.generate_hash(password)})
    db.commit()


# CODE VERIFICATION
async def verify_code(id, code, db: Session):
    return db.query(models.ResetPasswordCodes).filter(
        sqlalchemy.and_(models.ResetPasswordCodes.user_id == id,
                        models.ResetPasswordCodes.code == code)).first()


async def verify_code_auth(id, code, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_code(id, code, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})

# VERIFY CODE BY EMAIL


# UPDATE USER
async def update_user(id: int, payload: schemas.UserUpdate, db: Session):
    try:
        if not await read_user_by_id(id, db):
            raise schemas.NotFoundError('user not found')
        res = db.query(models.UserInfo).filter(models.UserInfo.user_id == id).update(
            payload.dict(exclude_unset=True).items())
        db.commit()
        if bool(res):
            return await read_user_by_id(id, db)
    except schemas.NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(
            status_code=409, detail="unique constraint failed on index")
    except schemas.ExpectationFailure:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def update_user_auth(id: int, payload: schemas.UserUpdate, token: str,
                           db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await update_user(id, payload, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# DELETE USER
async def delete_user(id: int, db):
    try:
        user = await read_user_by_id(id, db)
        if user:
            db.delete(user)
        db.commit()
        return True
    except schemas.ExpectationFailure:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def delete_user_auth(id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await delete_user(id, db)
        else:
            return schemas.UnAuthorised('Not qualified')
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})
