from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


router = APIRouter()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sel@localhost:5432/farmerlynkz"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

db = SessionLocal()
# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# READ STAFF DETAILS


@router.get("/classification")
async def read_classification_types(db: Session = Depends(get_db)):
    return await crud.read_classification_types(db)


@router.get("/croptypes")
async def read_crop_types(db: Session = Depends(get_db)):
    return await crud.read_crop_types(db)


@router.get("/")
async def read_crops(db: Session = Depends(get_db)):
    return await crud.read_crops(db)


@router.post("/classification")
async def create_classification_types(payload: schemas.create_classification_types,
                                      db: Session = Depends(get_db)):
    return await crud.create_classification_types(payload.classification_type, db)


@router.post("/croptypes")
async def create_crop_types(payload: schemas.create_crop_types, db: Session = Depends(get_db)):
    return await crud.create_crop_types(payload.classif_id, payload.crop_type, db)


@router.post("/")
async def create_crop(payload: schemas.create_crop, db: Session = Depends(get_db)):
    return await crud.create_crop(payload.classif_id, payload.croptype_id, payload.cropname, db)
