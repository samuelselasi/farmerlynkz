from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, APIRouter, Depends, APIRouter, HTTPException
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta, date
from pydantic import EmailStr, BaseModel, UUID4
from starlette.responses import JSONResponse
from database import SessionLocal, engine
from starlette.requests import Request
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models
import asyncio
import pytz



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

conf = ConnectionConfig(
    MAIL_USERNAME = "a4caa35d5e3fe6",
    MAIL_PASSWORD = "e77fca8df17a72",
    MAIL_FROM = "admin@aiti.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = False,
    MAIL_SSL = False,
    # USE_CREDENTIALS = True
)

fm = FastMail(conf)

background_tasks = BackgroundTasks()


async def background_send(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=models.template1.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send3(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Form",
            recipients=[item[1]],
            body=models.template2.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send_4(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=models.template3.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

def background_send_2(user_hash_list) -> JSONResponse:
    # print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Reminder)",
            recipients=[item[1]],
            body=models.template.format(url="http://localhost:4200/forms/start/harsh",hash=item[0]),
            subtype="html"
        )
        fm.send_message(message)        
        # background_tasks.add_task(fm.send_message,message)




async def simple_send(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Reminder)",
            recipients=[item[1]],
            body=models.template4.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )       
        await fm.send_message(message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})
        # background_tasks.add_task(fm.send_message,message)        



@router.post("/startreviewemail/")
async def start_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send(res, background_tasks)

@router.post("/midyearreviewemail/")
async def midyear_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send3(res, background_tasks)

@router.post("/endofyearreviewemail/")
async def end_0f_year_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_4(res, background_tasks)

@router.post("/emailreminder/")
async def email_reminder():
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await simple_send(res)     


jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}

db = SessionLocal()
deadline = db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'Start' """)
deadline = deadline.fetchall()
start_date = deadline[0][1]
end_date = deadline[0][2]
send_date = start_date - timedelta(3)

scheduler = AsyncIOScheduler()  
scheduler.add_job(func= email_reminder, trigger='date', run_date = send_date )
scheduler.start() 