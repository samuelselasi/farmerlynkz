from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from services.email import background_send
from database import SessionLocal, engine
from routers.phase1_router import models
from routers.staff_router import models
from routers.auth_router import models
from routers.appraiser import models
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

api = FastAPI(docs_url="/api/docs")

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
import pytz

jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=1)

def send_email():
    
    # return 'df'
    print("fill in your forms")

from datetime import datetime, timedelta

# scheduler.add_job(send_email, trigger = 'cron', month='1-2, 6-7,11-12', day='1st mon, 3rd fri', hour='0-2')

async def send_hash_email():
    background_tasks=BackgroundTasks()
    db = SessionLocal()
    res = db.execute(""" SELECT * FROM public.hash_table """)
    
    if res.rowcount:
        print('sd')
        await background_send(res.fetchall(), background_tasks)
    print('success')

scheduler.add_job(send_hash_email, trigger='interval', minutes=1)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

from routers.phase1_router import main as phase1
from routers.appraiser import main as appraiser
from routers.staff_router import main as staff
from routers.auth_router import main as auth

api.include_router(appraiser.router,prefix="/api/appraiser", tags=["appraiser"])
api.include_router(phase1.router,prefix="/api/review",tags=["review"])
api.include_router(staff.router,prefix="/api/staff",tags=["staff"])
api.include_router(auth.router,prefix="/api/user",tags=["user"])

@api.get("/")
def welcome():
    return "Reminders started"

@api.on_event("startup")
async def startup_event():
    scheduler.start()

@api.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


background_tasks = BackgroundTasks()

@api.post("/email")
async def send_staff_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    print('send_staff_email')
    print(dir(background_tasks))
    return await background_send(res, background_tasks)

@api.post("/test/test")
async def b():
    print('b')
    print(dir(background_tasks))
    return await background_send([{'email':'a@a.com','hash':'34242assdd'}], background_tasks)