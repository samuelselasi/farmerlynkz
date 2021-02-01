from datetime import datetime, time, timedelta
from typing import List, Optional
from pydantic import BaseModel


class FormBase(BaseModel):
    result_areas: str
    target: str 
    resources: str 
    appraisal_form_id: int
    annual_plan_id: int 
    status: int
    form_hash: str  

class AnnualAppraisal(BaseModel):
    grade: int
    comment: str 
    field: str 
    appraisal_form_id: int 
    status: int 
    annual_appraisal_id: int

class AppraisalForm(BaseModel):
    department: str 
    grade: int 
    position: str 
    appraisal_form_id:int 
    date: datetime
    staff_id: int

class create_appraisal_form(AppraisalForm):
    pass
class create_annual_plan(FormBase):
    pass
    
class create_annual_appraisal(AnnualAppraisal):
    pass
class UpdateForm(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase

class update_phase1(BaseModel):
    kra: Optional[FormBase]
    target: Optional[FormBase]
    resource_required: Optional[FormBase]

class get_Phase1(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase

class approve_phase1(BaseModel):
    # kra: FormBase
    # target: FormBase
    # resource_required: FormBase
    status:bool