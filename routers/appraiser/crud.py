from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException, jwt, sys
from ..user_router.crud import read_user_by_id
from starlette.responses import JSONResponse
from ..user_router.models import User
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends
from .. import email


# GET DEADLINES
async def read_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_start_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='Start'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_start_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_start_deadline_table(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_mid_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='Mid'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_mid_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_mid_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_end_deadline_table(db:Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline where deadline_type='End'; """) # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res

async def read_end_deadline_table_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if token_data:
            return await read_end_deadline_table(db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET APPRAISEES
async def read_appraiser_appraisees(user_id, db: Session):
    res = db.execute(""" SELECT public.get_list_of_appraisee(:user_id) """,{'user_id':user_id}) # GET APPRAISEE FROM DB FUNCTION
    return res.fetchall()  

async def read_appraiser_appraisees_auth(user_id:int, token:str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_appraiser_appraisees(user_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET COMPLETED
async def read_completed_list(supervisor:int, db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where supervisor=:supervisor and start_status=1""",{'supervisor':supervisor})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def read_completed_list_auth(supervisor:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_completed_list(supervisor, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


async def read_completed_list_admin(db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where start_status=1""")  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def read_completed_list_admin_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if data==1:
            return await read_completed_list_admin(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET APROVED
async def read_approved_forms(supervisor:int, db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where supervisor=:supervisor and start_status=1""",{'supervisor':supervisor}) # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def read_approved_forms_auth(supervisor:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_approved_forms(supervisor, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

async def read_approved_forms_admin(db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where start_status=1""") # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def read_approved_forms_admin_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if data==1:
            return await read_approved_forms_admin(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET WAITING APPROVAL
async def waiting_approval_list(supervisor:int, db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where supervisor=:supervisor and start_status=0 and target is not null and result_areas is not null and resources is not null""",{'supervisor':supervisor}) # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def waiting_approval_list_auth(supervisor:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await waiting_approval_list(supervisor, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"}) 

async def waiting_approval_list_admin(db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where start_status=0 and target is not null and result_areas is not null and resources is not null""") # GET FROM DB FUNCTION
    res = res.fetchall()
    return res 

async def waiting_approval_list_admin_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if data==1:
            return await waiting_approval_list_admin(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET INCOMPLETED
async def read_incomplete_list(supervisor:int, db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where supervisor=:supervisor and start_status=0 and target is null and result_areas is null and resources is null""",{'supervisor':supervisor}) # GET FROM DB FUNCTION
    res = res.fetchall()
    return res    

async def read_incomplete_list_auth(supervisor:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_incomplete_list(supervisor, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        

async def read_incomplete_list_admin(db:Session):
    res = db.execute("""SELECT * FROM view_users_form_details where start_status=0 and target is null and result_areas is null and resources is null""") # GET FROM DB FUNCTION
    res = res.fetchall()
    return res    

async def read_incomplete_list_admin_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if data==1:
            return await read_incomplete_list_admin(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

# GET SUPERVISORS
async def read_supervisors(db: Session):
    res = db.execute(""" SELECT user_id, first_name, middle_name, last_name FROM public.user_info; """) # GET FROM USERS TABLE
    res = res.fetchall()
    return res

async def read_supervisors_auth(token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_supervisors(db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# GET YEARLY DETAILS
async def read_yearly_form_deatails(staff_id:int, form_year:int, db:Session):
    res = db.execute(""" SELECT public.get_form_details_yearly(:staff_id, :form_year) """, {'staff_id':staff_id, 'form_year':form_year}) # GET FROM DB FUNCTION
    res = res.fetchall()
    return res

async def read_yearly_form_deatails_auth(staff_id:int, form_year:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token) 
        if token_data:
            return await read_yearly_form_deatails(staff_id, form_year, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"}) 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})        


# APPROVE FORM DETAILS
async def approve_form(appraisal_form_id:int, type_form:str, db:Session):
    res = db.execute(""" SELECT public.approve_form_details(:appraisal_form_id, :type_form) """, {'appraisal_form_id':appraisal_form_id, 'type_form':type_form}) # APPROVE FROM DB FUNCTION
    res = res.fetchall()
    db.commit()
    await email.main.annual_plan_approved(appraisal_form_id) # SEND APPROVED ANNUAL PLAN DETAILS TO STAFF'S EMAIL
    return res

async def approve_form_details_auth(appraisal_form_id:int, type_form:str, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await approve_form(appraisal_form_id, type_form, db)
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# CREATE APPRAISER DETAILS
async def create_deadline(deadline_type, start_date, ending, db:Session):
    res = db.execute("""insert into public.deadline(deadline_type,start_date,ending)
    values(:deadline_type, :start_date, :ending) on conflict (deadline_type) do 
	update set deadline_type = EXCLUDED.deadline_type, start_date = EXCLUDED.start_date, ending = EXCLUDED.ending;""",
    {'deadline_type':deadline_type, 'start_date':start_date, 'ending':ending}) # INSERT INTO DEADLINE TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been created"})

async def create_deadline_auth(deadline_type:str, start_date:str, ending:str, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        if data==1:
            return await create_deadline(deadline_type, start_date, ending, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# UPDATE APPRAISER DETAILS
async def update_deadline(deadline:schemas.update_deadline, db:Session):
    res = db.execute("""UPDATE public.deadline
	SET deadline_id = :deadline_id, deadline_type = :deadline_type, start_date = :start_date, ending = :ending
	WHERE deadline_id = :deadline_id;""",
    {'deadline_id':deadline.deadline_id, 'deadline_type':deadline.deadline_type, 'start_date':deadline.start_date, 'ending':deadline.ending}) #UPDATE IN TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "deadline has been updated"})

async def update_deadline_auth(deadline:schemas.update_deadline, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data==1:
            return await update_deadline(deadline, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})


# DELETE APPRAISER DETAILS
async def delete_deadline(deadline_id:int, db:Session):
    res = db.execute("""DELETE FROM public.deadline
	WHERE deadline_id=:deadline_id;""",
    {'deadline_id':deadline.deadline_id})
    db.commit() 
    return JSONResponse(status_code=200, content={"message": "deadline has been deleted"}) #DELETE FROM TABLE

async def delete_deadline_auth(deadline_id:int, token:str, db:Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data==1:
            return await delete_deadline(deadline_id, db)
        else:
            return UnAuthorised('Not qualified') 
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})
        