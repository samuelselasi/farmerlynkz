from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from starlette.requests import Request
from fastapi import BackgroundTasks
from pydantic import EmailStr
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME = "a97a6351fa551d",
    MAIL_PASSWORD = "8608ab42c0b55f",
    MAIL_FROM = "a@a.com",
    MAIL_PORT = 25,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

fm = FastMail(conf)

template = """
<p>Hi this test mail using BackgroundTasks, thanks for using Fastapi-mail</p> 
<a href="{url}/{hash}" target="_blank">click this link to fill form</a>
"""

def background_send(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=[item['email']],
            body=template.format(url="https://google.com",hash=item['hash']),
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
