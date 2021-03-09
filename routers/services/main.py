from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, APIRouter, Depends
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.responses import JSONResponse
from database import SessionLocal, engine
from pydantic import EmailStr, BaseModel
from starlette.requests import Request
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import List
from main import get_db


from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional

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
    MAIL_TLS = False,
    MAIL_SSL = False,
    # USE_CREDENTIALS = True
)




fm = FastMail(conf)

template = """
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



async def background_send(user_hash_list, background_tasks) -> JSONResponse:
    print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=template.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send3(user_hash_list, background_tasks) -> JSONResponse:
    # print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Form",
            recipients=[item[1]],
            body=template2.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)


# class EmailSchema(BaseModel):
#     email: List[EmailStr]
# @api.post("/send email")
# from utils import generate_hash
# return JSONResponse(status_code=200, content={"message": "email has been sent"})    
# await fm.send_message(message)
# x = lambda length: generate_hash(length)
# user_hash_list = [{"email":"test@mail.com","hash":x(15)}, {"email":"sel@mail.com","hash":x(15)}, {"email":"sam@mail.com","hash":x(15)}, {"email":"unique@mail.com","hash":x(15)}, {"email":"smsel@mail.com","hash":x(15)}, {"email":"asare@mail.com","hash":x(15)}, {"email":"shit@mail.com","hash":x(15)}, {"email":"ea@mail.com","hash":x(15)}, {"email":"tst@mail.com","hash":x(15)}]




def background_send_2(user_hash_list) -> JSONResponse:
    # print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=template.format(url="http://localhost:4200/forms/start/harsh",hash=item[0]),
            subtype="html"
        )
        fm.send_message(message)        
        # background_tasks.add_task(fm.send_message,message)

async def background_send_4(user_hash_list, background_tasks) -> JSONResponse:
    print(user_hash_list)
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=template3.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)


def simple_send(user_hash_list):
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=template.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        )
        fm.send_message(message)        
        # background_tasks.add_task(fm.send_message,message)        



@router.post("/startreviewemail/")
async def send_start_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    return await background_send(res, background_tasks)

@router.post("/midyearreviewemail/")
async def send_midyear_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    return await background_send3(res, background_tasks)

@router.post("/endofyearreviewemail/")
async def send_end_0f_year_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    return await background_send_4(res, background_tasks)

@router.post("/test/test")
async def b(background:BackgroundTasks):
    # print('b')
    # print(dir(background_tasks))
    return await background_send([('afsd', 'a@test.com')], background)