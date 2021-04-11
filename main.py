from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, FastAPI, WebSocket, WebSocketDisconnect
from database import SessionLocal, engine, SQLALCHEMY_DATABASE_URL, metadata
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from schedulers import scheduler
from sockets import manager
import pytz, os, config


api = FastAPI(docs_url="/api/docs")
# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

settings = config.Settings()

# GIVE PERMISSION TO FRONTEND
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


from routers.auth_router import models
from routers.user_router import models
models.Base.metadata.create_all(bind=engine)

# IMPORT ALL ROUTERS
from routers.phase1_router import main as phase1
from routers.phase2_router import main as phase2
from routers.phase3_router import main as phase3
from routers.appraiser import main as appraiser
from routers.staff_router import main as staff
from routers.auth_router import main as auth
from routers.user_router import main as user
from routers.email import main as email

# CUSTOMIZE ALL ENDPOINT HEADERS
api.include_router(auth.router, prefix="/auth", tags=["User Login"])
api.include_router(user.router, prefix="/user", tags=["User"])
api.include_router(staff.router,prefix="/api/staff",tags=["Staff"])
api.include_router(appraiser.router,prefix="/api/appraiser", tags=["Appraiser"])
api.include_router(phase1.router,prefix="/api/review",tags=["Start Review"])
api.include_router(phase2.router, prefix="/api/midyearreview", tags=["Mid-Year Review"])
api.include_router(phase3.router, prefix="/api/endofyearreview", tags=["End of Year Review"])
api.include_router(email.router, prefix="/email", tags=["E-mails"])


@api.get("/")
def welcome():
    return "Reminders started"
