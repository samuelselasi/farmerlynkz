import utils
import jwt
import sys
from fastapi import HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas


async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti ==
                                               token).first()  # GET EXPIRED TOKENS FROM DB
    if res is None:
        return False
    return True


# GET STAFF DETAILS
async def read_classification_types(db: Session):
    res = db.execute(""" SELECT * FROM public.classification_types; """)
    res = res.fetchall()
    return res


async def read_classification_types_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_classification_types(db)
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


async def read_crop_types(db: Session):
    res = db.execute(""" SELECT * FROM public.crop_types; """)
    res = res.fetchall()
    return res


async def read_crop_types_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_crop_types(db)
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


async def read_crops(db: Session):
    res = db.execute(""" SELECT * FROM public.crops; """)
    res = res.fetchall()
    return res


async def read_crops_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_crops(db)
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


# CREATE CLASSIFICATION TYPE
async def create_classification_types(classification_type, db: Session):
    db.execute("""insert into public.classification_types(classification_type)
    VALUES(:classification_type)""",
               {'classification_type': classification_type})  # INSERT STAFF DETAILS INTO TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Crop classification created"})


async def create_classification_types_auth(classification_type, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await create_classification_types(classification_type, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# CREATE CROP TYPE
async def create_crop_types(classif_id, crop_type, db: Session):
    db.execute("""insert into public.crop_types(classif_id, crop_type)
    VALUES(:classif_id, :crop_type)""",
               {'classif_id': classif_id, 'crop_type': crop_type})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Crop type created"})


async def create_crop_types_auth(classif_id, crop_type, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await create_crop_types(classif_id, crop_type, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# CREATE CROP
async def create_crop(classif_id, croptype_id, cropname, db: Session):
    db.execute("""insert into public.crops(classif_id, croptype_id, cropname)
    VALUES(:classif_id, :croptype_id, :cropname)""",
               {'classif_id': classif_id, 'croptype_id': croptype_id, 'cropname': cropname})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Crop created"})


async def create_crop_auth(classif_id, croptype_id, cropname, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise schemas.UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await create_crop(classif_id, croptype_id, cropname, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except schemas.UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})
