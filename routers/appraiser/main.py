from fastapi import APIRouter, Depends, HTTPException
from main import get_db, oauth2_scheme
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas



router = APIRouter()


# GET APPRAISEES
@router.get("/Appraisees/{user_id}/")
async def read_appraiser_appraisees(user_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_appraiser_appraisees_auth(user_id, token, db)


# GET APPROVED
@router.get("/approved/start/")
async def read_approved_forms( user_id:int, token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_approved_forms_auth(user_id, token, db)

@router.get("/approved/start/admin/")
async def read_approved_forms_admin( token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_approved_forms_admin_auth(token, db)

@router.get("/approved/mid/")
async def read_approved_forms( user_id:int, deadline='Mid', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_approved_forms_auth( deadline, user_id, token, db)

@router.get("/approved/end/")
async def read_approved_forms(user_id:int, deadline='End', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_approved_forms_auth( deadline, user_id, token, db)



# GET DISAPPROVED
@router.get("/disapproved/start/")
async def read_disapproved_forms( user_id:int, token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_disapproved_forms_auth(user_id, token, db)

@router.get("/approved/start/admin/")
async def read_approved_forms_admin( token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_approved_forms_admin_auth(token, db)

@router.get("/approved/mid/")
async def read_approved_forms( user_id:int, deadline='Mid', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_approved_forms_auth( deadline, user_id, token, db)

@router.get("/approved/end/")
async def read_approved_forms(user_id:int, deadline='End', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_approved_forms_auth( deadline, user_id, token, db)


# GET COMPLETED
@router.get("/completedlist/start/")
async def read_completed_list(user_id:int, token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_completed_list_auth(user_id, token, db)

@router.get("/completedlist/start/admin/")
async def read_completed_list_admin(token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_completed_list_admin_auth(token, db)

@router.get("/completedlist/mid/")
async def read_completed_list(user_id:int, deadline='Mid', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_completed_list_auth( deadline, user_id, token, db)

@router.get("/completedlist/end/")
async def read_completed_list(user_id:int, deadline='End', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_completed_list( deadline, user_id, token, db)


# GET WAITING APPROVAL
@router.get("/waitingapproval/start/")
async def waiting_approval_list(user_id:int, token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.waiting_approval_list_auth(user_id, token, db)

@router.get("/waitingapproval/start/admin")
async def waiting_approval_list_admin(token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.waiting_approval_list_admin_auth(token, db)

@router.get("/waitingapproval/mid/")
async def waiting_approval_list(user_id:int, deadline='Mid', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.waiting_approval_list_auth( deadline, user_id, token, db)

@router.get("/waitingapproval/end/")
async def waiting_approval_list(user_id:int, deadline='End', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.waiting_approval_list_auth( deadline, user_id, token, db)


# GET INCOMPLETED
@router.get("/incompletedlist/start/")
async def read_incompleted_list(user_id:int, token:str=Depends(oauth2_scheme),  db:Session=Depends(get_db)):
    return await crud.read_incomplete_list_auth(user_id, token, db)

@router.get("/incompletedlist/start/admin/")
async def read_incompleted_list_admin(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_incomplete_list_admin_auth(token, db)

@router.get("/incompletedlist/mid/")
async def read_incompleted_list(user_id:int, deadline='Mid', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_incomplete_list_auth( deadline, user_id, token, db)  

@router.get("/incompletedlist/end/")
async def read_incompleted_list(user_id:int, deadline='End', token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_incomplete_list_auth( deadline, user_id, token, db)  



# READ DEADLINES
@router.get("/deadline/")
async def read_deadline_table(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_deadline_table_auth(token, db)

@router.get("/deadline/start/")
async def read_start_deadline(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_start_deadline_table_auth(token, db)

@router.get("/deadline/mid/")
async def read_mid_deadline(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_mid_deadline_table_auth(token, db)

@router.get("/deadline/end/")
async def read_end_deadline(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_end_deadline_table_auth(token, db)


# GET SUPERVISORS
@router.get("/supervisors/")
async def read_supervisors(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_supervisors_auth(token, db)


# GET YEARLY DETAILS
@router.get("/yearlyformdetails/{staff_id}/{form_year}")
async def read_yearly_form_deatails(staff_id:int, form_year:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.read_yearly_form_deatails_auth(staff_id, form_year, token, db)


# APPROVE FORM DETAILS
@router.get("/approveform/{appraisal_form_id}/")
async def approve_form_details(appraisal_form_id:int, type_form='Start', token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.approve_form_details_auth(appraisal_form_id, type_form, token, db)

@router.post("/disapproveform/{appraisal_form_id}/")
async def disapprove_form_details(appraisal_form_id:int, supervisor_comment:str, type_form='Start', token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.disapprove_form_details_auth(appraisal_form_id, supervisor_comment, type_form, token, db)


@router.get("/approveform/mid/{appraisal_form_id}/")
async def approve_form_details(appraisal_form_id:int, type_form='Mid', token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.approve_form_details_auth(appraisal_form_id, type_form, token, db)

@router.get("/approveform/end/{appraisal_form_id}/")
async def approve_form_details(appraisal_form_id:int, type_form='End', token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.approve_form_details_auth(appraisal_form_id, type_form, token, db)



# CREATE APPRAISER DETAILS
@router.post("/deadline/")
async def create_deadline(payload:schemas.create_deadline, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.create_deadline_auth(payload.deadline_type, payload.start_date, payload.ending, token, db)



# UPDATE APPRAISER DETAILS
@router.put("/deadline/")
async def update_deadline_table(deadline:schemas.update_deadline, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.update_deadline_auth(deadline, token, db)



# DELETE APPRAISER DETAILS
@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id:int, token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return await crud.delete_deadline_auth(deadline_id, token, db) 