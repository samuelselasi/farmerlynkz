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
from . import main
import asyncio
import pytz



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
apparisal forms will be due to start in three days time.</p>

<p>Your appraisal form details will be provided and made available to you soon. Please
check your mail for a link on the due date.</p>

<strong><p>Please fill the form by opening the link provided.</strong></br>
<a href="{url}/{hash}" target="_blank">click this link to fill form</a> </p>

You are expected to access and fill the form provided in
<strong>three days time  </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""

template5 = """
<font size = "+2">
<h1> <i> Appraoisal Form Details </i> </h1>

<p>Dear Sir/Madam,</p>

<p>Your start of year review forms have been inspected
approved by your supervisor.</p>

<p>Your appraisal form details will be provided and made available to you for future 
reference in completing the mid-year and end of year review forms.</p>

<strong><p>View your form details to keep track of your progress.</strong></br>
            grade = {grade}</br>
            roles = {roles}</br>
            score = {score}</br>
            gender = {gender}</br>
            target = {target}</br>
            weight = {weight}</br>
            comment = {comment}</br>
            remarks = {remarks}</br>
            last name = {lastname}</br>
            staff id = {staff_id}</br>
            first name ={firstname}</br>
            position = {positions}</br>
            resources = {resources}</br>
            assessment = {assessment}</br>
            department = {department}</br>
            end status = {end_status}</br>
            mid status = {mid_status}</br>
            middle name = {middlename}</br>
            supervisor = {supervisor}</br>
            result areas = {result_areas}</br>
            start status ={start_status}</br>
            appraisal year = {appraisal_year}</br>
            progress review ={progress_review}</br>
            supervisor name = {supervisor_name}</br>
            role = {role_description}</br>
            supervisor email = {supervisor_email}</br>
            appraisal form id = {appraisal_form_id} </p></br>

The forms will be avilable untill the start of the
<strong>Mid-Year Review process  </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""

template6 = """
<font size = "+2">
<h1> <i> Approve Appraisee Form(Reminder) </i> </h1>

<p>Dear Supervisor,</p>

<p>Please review and approve forms of appraisee under you
for the start of the yearly appraisal form details.</p>

<p>The appraisal form details will be provided and made available to 
you  below.</p>

<strong><p>Kindly review the form details.</strong></br>
            
            email = {email}</br>
            roles = {roles}</br>
            score = {score}</br>
            gender = {gender}</br>
            target = {target}</br>
            weight = {weight}</br>
            comment = {comment}</br>
            remarks = {remarks}</br>
            last name = {lastname}</br>
            staff id = {staff_id}</br>
            first name ={firstname}</br>
            position = {positions}</br>
            resources = {resources}</br>
            assessment = {assessment}</br>
            department = {department}</br>
            end status = {end_status}</br>
            mid status = {mid_status}</br>
            middle name = {middlename}</br>
            supervisor = {supervisor}</br>
            result areas = {result_areas}</br>
            start status ={start_status}</br>
            appraisal year = {appraisal_year}</br>
            progress review ={progress_review}</br>
            supervisor name = {supervisor_name}</br>
            role = {role_description}</br>
            supervisor email = {supervisor_email}</br>
            appraisal form id = {appraisal_form_id} </p></br>

You are expected to review and approve the form details
<strong>before the start of Mid-Year Review  </strong> <br/>

Thank You. <br/>
Appraiser-App Admin </p> 
</font>

"""