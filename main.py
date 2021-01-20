from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine

from routers.auth_router import models

from routers.staff_router import models
from routers.phase1_router import models

from fastapi.security import OAuth2PasswordBearer

from services import email

from fastapi import BackgroundTasks


api = FastAPI(docs_url="/api/docs")

origins = ["http://localhost/*","http://localhost:8080","http://localhost:3000"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import pytz

from apscheduler.schedulers.background import BackgroundScheduler

# from apscheduler.jobstores.mongodb import MongoDBJobStore

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
# job schedular


jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=1)

def a():
    # return 'df'
    print("fill in your forms")

from datetime import datetime, timedelta

scheduler.add_job(a, trigger = 'cron', month='1-2, 6-7,11-12', day='1st mon, 3rd fri', hour='0-2')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")


from routers.auth_router import main as auth

from routers.staff_router import main as staff

from routers.phase1_router import main as phase1


api.include_router(auth.router,prefix="/api/user",tags=["user"])

api.include_router(phase1.router,prefix="/api/phase1",tags=["phase1"])

api.include_router(staff.router,prefix="/api/staff",tags=["staff"])


@api.get("/")
def welcome():
    return "Reminders started"



@api.on_event("startup")
async def startup_event():
    scheduler.start()



@api.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()



@api.post("/")
async def Email(background_tasks:BackgroundTasks):
    await email.background_send(email.user_hash_list, background_tasks)
    return "email has been sent"


