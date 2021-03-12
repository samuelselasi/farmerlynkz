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

async def background_send_2(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Form",
            recipients=[item[1]],
            body=models.template2.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send_3(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=models.template3.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send_4(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form Details",
            recipients=[item["email"]],
            body=models.template5.format( email= [item["email"]],
            grade= [item["grade"]],
            roles= [item["roles"]],
            score= [item["score"]],
            gender= [item["gender"]],
            target= [item["target"]],
            weight= [item["weight"]],
            comment= [item["comment"]],
            remarks= [item["remarks"]],
            lastname= [item["lastname"]],
            staff_id= [item["staff_id"]],
            firstname= [item["firstname"]],
            positions= [item["positions"]],
            resources= [item["resources"]],
            assessment= [item["assessment"]],
            department= [item["department"]],
            end_status= [item["end_status"]],
            mid_status= [item["mid_status"]],
            middlename= [item["middlename"]],
            supervisor= [item["supervisor"]],
            result_areas= [item["result_areas"]],
            start_status= [item["start_status"]],
            appraisal_year= [item["appraisal_year"]],
            progress_review= [item["progress_review"]],
            supervisor_name= [item["supervisor_name"]],
            role_description= [item["role_description"]],
            supervisor_email= [item["supervisor_email"]],
            appraisal_form_id= [item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        # return JSONResponse(status_code=200, content={"message": "email has been sent"})

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
    return await background_send_2(res, background_tasks)

@router.post("/endofyearreviewemail/")
async def end_0f_year_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_3(res, background_tasks)

@router.post("/startformdetails/")
async def start_form_details(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT public.get_list_of_approved_form('Start', 1)""")
    res = res.first()[0]
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