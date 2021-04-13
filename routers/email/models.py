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
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear All,</p> </h3> </div>
               

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
                        Performance Planning Form
                    </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""


template2 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear All,</p> </h3> </div>
               

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
                    Appraiser-App Admin
                </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template3 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear All,</p> </h3> </div>
               

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
                            Appraiser-App Admin
                    </p>
            # </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template4 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear All,</p> </h3> </div>
               

                    <p>As a requirement for the completion
                    of your Annual appraisal form, the End of Year Review
                    Form is provided to all staff.</p>

                    <p>Your End of Year Review form for the year has
                    been made available to you.</p>

                    <strong><p>Please fill the form by opening the link provided.</strong></br>
                

                    You are expected to access and fill the form by
                    <strong>the end of this month </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                    </p>

                    </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template5 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Sir/Madam,</p> </h3>

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
                        Appraiser-App Admin
                     </p>

            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template6 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Supervisor,</p> </h3>

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
                Appraiser-App Admin
             </p>

            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template7 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3>  <p>Dear Sir/Madam,</p>  </h3>
               

                   

                            <p>As a staff requirement, you are reminded that the yearly
                            apparisal form will end in 5 days time.</p>

                            <p>Your appraisal form details have been provided and made available to you in this mail. Please
                            follow the link to complete your form.</p>

                            <strong><p>Please fill the form by opening the link provided.</strong></br>
                            <a href="{url}" target="_blank">click this link to fill form</a> </p>

                            You are expected to access and fill the form provided in
                            <strong>five days time  </strong> <br/>

                            Thank You. <br/>
                            Appraiser-App Admin
                        </p>

            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""

template8 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Sir/Madam,</p> </h3> </div>
               

                   

                        <p>As a staff requirement, you are reminded that the yearly
                        apparisal form will end in 4 days time.</p>

                        <p>Your appraisal form details have been provided and made available to you in this mail. Please
                        follow the link to complete your form.</p>

                        <strong><p>Please fill the form by opening the link provided.</strong></br>
                        <a href="{url}" target="_blank">click this link to fill form</a> </p>

                        You are expected to access and fill the form provided in
                        <strong>four days time  </strong> <br/>

                        Thank You. <br/>
                        Appraiser-App Admin
                    </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template9 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Sir/Madam,</p> </h3>

                        <p>As a staff requirement, you are reminded that the yearly
                        apparisal form will end in 3 days time.</p>

                        <p>Your appraisal form details have been provided and made available to you in this mail. Please
                        follow the link to complete your form.</p>

                        <strong><p>Please fill the form by opening the link provided.</strong></br>
                        <a href="{url}" target="_blank">click this link to fill form</a> </p>

                        You are expected to access and fill the form provided in
                        <strong>three days time  </strong> <br/>

                        Thank You. <br/>
                        Appraiser-App Admin
                    </p>


            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""

template10 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p><p>Dear Sir/Madam,</p></h3>

                    <p>As a staff requirement, you are reminded that the yearly
                    apparisal form will end in 2 days time.</p>

                    <p>Your appraisal form details have been provided and made available to you in this mail. Please
                    follow the link to complete your form.</p>

                    <strong><p>Please fill the form by opening the link provided.</strong></br>
                    <a href="{url}" target="_blank">click this link to fill form</a> </p>

                    You are expected to access and fill the form provided in
                    <strong>two days time  </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                </p>


            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template11 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Sir/Madam,</p> </h3>

                    <p>As a staff requirement, you are reminded that the yearly
                    apparisal form will end today.</p>

                    <p>Your appraisal form details have been provided and made available to you in this mail. Please
                    follow the link to complete your form.</p>

                    <strong><p>Please fill the form by opening the link provided.</strong></br>
                    <a href="{url}" target="_blank">click this link to fill form</a> </p>

                    You are expected to access and fill the form provided
                    <strong>by the end of today  </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template12 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Supervisor,</p></h3>

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
            <strong>before the start of Mid-Year Review in 5 days time  </strong> <br/>

            Thank You. <br/>
            Appraiser-App Admin </p>
                        </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template13 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear All,</p> </h3> </div>
               

                    <p>As a requirement for the completion
                        of your Annual appraisal form, the performance planning
                        form is provided to all staff.</p>
                       
                        <p>Your performance planning form for the year has
                        been made available to you.</p>
                       
                        <strong><p>Please fill the form by opening the link provided.</strong></br>
                        
                       
                        You are expected to access and fill the form by
                        <strong>the end of this month </strong> <br/>
                       
                        Thank You. <br/>
                        Performance Planning Form
                    </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""

template14 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Supervisor,</p></h3>

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
                        <strong>before the start of Mid-Year Review in 4 days time  </strong> <br/>

                        Thank You. <br/>
                        Appraiser-App Admin
                    </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""

template15 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3>  <p>Dear Supervisor,</p> </h3>
               

                 

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
                    <strong>before the start of Mid-Year Review in 4 days time  </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                  </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""

template16 =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3><p>Dear Supervisor,</p> </h3>

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
                    <strong>before the start of Mid-Year Review today  </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                </p>

            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""

template17 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
           

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
        <img src="https://assets.codepen.io/210284/h1_1.gif" width="300" height="230" style="display: block;" />
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
            </td>
        </tr>
        <tr>
            <td style="color: #153643; font-family: Arial, sans-serif; font-size: 22px; line-height: 24px; padding: 20px 0 30px 0;">
            <!-- <p style="margin: 0;"><font style= "size :2, text-decoration:"> -->

                <img alt="aiti.png" src="https://www.aiti-kace.com.gh/sites/default/files/aiti.png" style="width:199px;height:69px;">
       
                <h3> <p>Dear Supervisor,</p> </h3>
               

                   

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
                    <strong>before the start of Mid-Year Review today  </strong> <br/>

                    Thank You. <br/>
                    Appraiser-App Admin
                 </p>
            </p>
           
            </p>
 
            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#70bbd9" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; Aiti<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>

"""
