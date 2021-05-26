from fastapi import BackgroundTasks, APIRouter, Depends, APIRouter
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from starlette.responses import JSONResponse
from database import SessionLocal
from sqlalchemy.orm import Session
from main import settings

# IMPORT EMAILTENPLATES

from static.email_templates.template_3 import template3 


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SETUP MAILTRAP CONNECTION
fm = FastMail(
    ConnectionConfig(
        MAIL_USERNAME = settings.MAIL_USERNAME,
        MAIL_PASSWORD = settings.MAIL_PASSWORD,
        MAIL_FROM = settings.MAIL_FROM,
        MAIL_PORT = settings.MAIL_PORT,
        MAIL_SERVER = settings.MAIL_SERVER,
        MAIL_TLS = settings.MAIL_TLS,
        MAIL_SSL = settings.MAIL_SSL
    )
)

# DEFINE BACKGROUND TASKS
background_tasks = BackgroundTasks()


# BACKGROUND TASKS(WITHOUT SCHEDULER)

# START END OF YEAR REVIEW
async def background_send_3(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=template3.format(url=settings.START_URL,hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# BACKGROUND TASKS(WITH SCHEDULER)

# EMAIL ENDPOINTS FOR MANUALLY SENT EMAILS

# SEND END OF YEAR LINK TO ALL STAFF
@router.post("/endofyearreviewemail/")
async def start_end_0f_year_review_(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_3(res, background_tasks)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISEE
 
# END OF YEAR

# # @router.post("/threedaysreminder/")
# async def three_days_to_end_reminder():
#     res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
#     res = res.fetchall()
#     return await background_send_20(res)   

# # @router.post("/startday/")
# async def start_end_year_review():
#     res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
#     res = res.fetchall()
#     return await background_send_26(res)  

# # @router.post("/lastfivedaysreminder/")
# async def last_five_days_to_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
#     res = res.first()[0]
#     return await background_send_21(res)

# # @router.post("/lastfourdaysreminder/")
# async def last_four_days_to_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
#     res = res.first()[0]
#     return await background_send_22(res)

# # @router.post("/lastthreedaysreminder/")
# async def last_three_days_to_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
#     res = res.first()[0]
#     return await background_send_23(res)

# # @router.post("/lasttwodaysreminder/")
# async def last_two_days_to_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
#     res = res.first()[0]
#     return await background_send_24(res)

# # @router.post("/lastdayreminder/")
# async def last_day_to_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
#     res = res.first()[0]
#     return await background_send_25(res)    


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISER


# END OF YEAR

# # @router.post("/approveendyearreview/")
# async def approve_end_year_review(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "create_mid_year_review" FUNCTION IN phase_2 Router, crud.py 
#     res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM  
#     res = res.fetchall()
#     return await background_send_36(res)

# # @router.post("/midyearreviewapproved/")
# async def end_year_review_approved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
#     res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
#     res = res.fetchall()
#     return await background_send_32(res)

# # @router.post("/endyearreviewdisapproved/")
# async def end_year_review_disapproved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
#     res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email, midyear_review_comment FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
#     res = res.fetchall()
#     return await background_send_38(res)

# # @router.post("/lastfivedaystoapprovereminder/")
# async def last_five_days_to_approve_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
#     res = res.first()[0]
#     return await background_send_27(res)

# # @router.post("/lastfourdaystoapprovereminder/")
# async def last_four_days_to_approve_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
#     res = res.first()[0]
#     return await background_send_28(res)

# # @router.post("/lastthreedaystoapprovereminder/")
# async def last_three_days_to_approve_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
#     res = res.first()[0]
#     return await background_send_29(res)

# # @router.post("/lasttwodaystoapprovereminder/")
# async def last_two_days_to_approve_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
#     res = res.first()[0]
#     return await background_send_30(res)

# # @router.post("/lastdaytoapprovereminder/")
# async def last_day_to_approve_end_reminder():
#     res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
#     res = res.first()[0]
#     return await background_send_31(res)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}

#  DEADLINES
db=SessionLocal()
end_deadline=db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'End' """)
end_deadline=end_deadline.fetchall()


# DATES 

end_start_date=end_deadline[0][1]
end_end_date=end_deadline[0][2]
end_send_date=end_start_date-timedelta(3)
end_send_date_2=end_end_date-timedelta(5)
end_send_date_3=end_end_date-timedelta(4)
end_send_date_4=end_end_date-timedelta(3)
end_send_date_5=end_end_date-timedelta(2)
end_send_date_6=end_end_date

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# JOB SCHEDULER

# END
scheduler = AsyncIOScheduler()  
# scheduler.add_job(func=three_days_to_end_reminder, trigger='date', run_date=end_send_date)
# scheduler.add_job(func=start_end_year_review, trigger='date', run_date=end_start_date)
# scheduler.add_job(func=last_five_days_to_end_reminder, trigger='date', run_date=end_send_date_2)
# scheduler.add_job(func=last_four_days_to_end_reminder, trigger='date', run_date=end_send_date_3)
# scheduler.add_job(func=last_three_days_to_end_reminder, trigger='date', run_date=end_send_date_4)
# scheduler.add_job(func=last_two_days_to_end_reminder, trigger='date', run_date=end_send_date_5)
# scheduler.add_job(func=last_day_to_end_reminder, trigger='date', run_date=end_send_date_6)
# scheduler.add_job(func=last_five_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_2)
# scheduler.add_job(func=last_four_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_3)
# scheduler.add_job(func=last_three_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_4)
# scheduler.add_job(func=last_two_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_5)
# scheduler.add_job(func=last_day_to_approve_end_reminder, trigger='date', run_date=end_send_date_6)

scheduler.start() 