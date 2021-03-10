from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, APIRouter, Depends, APIRouter, HTTPException
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from pydantic import EmailStr, BaseModel, UUID4
from starlette.responses import JSONResponse
from database import SessionLocal, engine
from datetime import datetime, timedelta, date
from starlette.requests import Request
from sqlalchemy.orm import Session
from typing import List, Optional
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
    MAIL_USERNAME = "a97a6351fa551d",
    MAIL_PASSWORD = "8608ab42c0b55f",
    MAIL_FROM = "admin@aiti.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

fm = FastMail(conf)

template1 = """
<font size = "+2">
<h1> <i> Performance Planning Form </i> </h1>

<p>Hello Sir/Madam,</p>

<p>As a requirement for the completion
of your Annual appraisal form, the performance planning
form is provided to all staff.</p>

<p>Your performance planning form for the year has
been made available to you.</p>

<strong><p>Please fill the form by opening the link provided.</strong></br>
<a href="{url}/{hash}" target="_blank">click this link to fill form</a> </p>

You are expected to access and fill the form by
<strong>the end of this month </strong> <br/>

Thank You. <br/>
Performance Planning Form </p> 
</font>

"""

template2 = """
<font size = "+2">
<h1> <i> Mid Year Review Form </i> </h1>

<p>Dear All,</p>

<p>As a requirement for the completion
of your Annual appraisal form, the Mid-Year Review
form is provided to all staff.</p>

<p>Your Mid-Year Review form for the year has
been made available to you.</p>

<strong><p>Please fill the form by opening the link provided.</strong></br>
<a href="{url}/{hash}" target="_blank">click this link to fill form</a> </p>

You are expected to access and fill the form by
<strong>the end of this month </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""

template3 = """
<font size = "+2">
<h1> <i> End Of Year Review Form </i> </h1>

<p>Dear All,</p>

<p>As a requirement for the completion
of your Annual appraisal form, the End of Year Review
Form is provided to all staff.</p>

<p>Your End of Year Review form for the year has
been made available to you.</p>

<strong><p>Please fill the form by opening the link provided.</strong></br>
<a href="{url}/{hash}" target="_blank">click this link to fill form</a> </p>

You are expected to access and fill the form by
<strong>the end of this month </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""

template4 = """
<font size = "+2">
<h1> <i> Appraoisal Form (Reminder) </i> </h1>

<p>Dear All,</p>

<p>As a staff requirement, you are reminded that the yearly
apparisal forms will be due to start soon.</p>

<p>Your appraisal form details will be provided and made available to you soon. Please
check your mail for a link on the due date.</p>

<strong><p>Please fill the form by opening the link provided.</strong></br>
<a href="{url}/{hash}" target="_blank">click this link to fill form</a> </p>

You are expected to access and fill the form by
<strong>the end of this month </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""
background_tasks = BackgroundTasks()

async def background_send(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=template1.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send3(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Form",
            recipients=[item[1]],
            body=template2.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def background_send_4(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=template3.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})

def background_send_2(user_hash_list) -> JSONResponse:
    # print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Reminder)",
            recipients=[item[1]],
            body=template.format(url="http://localhost:4200/forms/start/harsh",hash=item[0]),
            subtype="html"
        )
        fm.send_message(message)        
        # background_tasks.add_task(fm.send_message,message)




async def simple_send(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Reminder)",
            recipients=[item[1]],
            body=template4.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )       
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
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

@router.post("/test/test")
async def b(background:BackgroundTasks):
    # print('b')
    # print(dir(background_tasks))
    return await background_send([('afsd', 'a@test.com')], background)



jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}

db = SessionLocal()


@router.post("/testemail")
async def send_hash_email(db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await simple_send(res) 
# scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=1)

scheduler = AsyncIOScheduler()  
scheduler.add_job(func= send_hash_email, trigger='interval', minutes=1)
scheduler.start() 