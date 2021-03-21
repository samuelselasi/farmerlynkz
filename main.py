from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import pytz


api = FastAPI(docs_url="/api/docs")

origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from routers.phase1_router import main as phase1
from routers.phase2_router import main as phase2
from routers.phase3_router import main as phase3
from routers.appraiser import main as appraiser
from routers.auth_router import main as auth
from routers.services import main as email
from routers.login_router import main as login

api.include_router(email.router, prefix="/email", tags=["E-mails"])
api.include_router(auth.router,prefix="/api/staff",tags=["Staff"])
api.include_router(appraiser.router,prefix="/api/appraiser", tags=["Appraiser"])
api.include_router(phase1.router,prefix="/api/review",tags=["Start Review"])
api.include_router(phase2.router, prefix="/api/midyearreview", tags=["Mid-Year Review"])
api.include_router(phase3.router, prefix="/api/endofyearreview", tags=["End of Year Review"])
api.include_router(login.router, prefix="/login", tags=["Login"])

@api.get("/")
def welcome():
    return "Reminders started"
