from typing import List, Optional
from pydantic import BaseModel


class FormBase(BaseModel):
    kra: str
    target: str
    resource_required: str
    form_id: int
class create_review_start(FormBase):
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