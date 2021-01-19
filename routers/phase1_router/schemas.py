from typing import List, Optional

from pydantic import BaseModel





class FormBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    body: List[str]



class create_phase1(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase



class update_phase1(BaseModel):
    kra: Optional[FormBase]
    target: Optional[FormBase]
    resource_required: Optional[FormBase]


class approve_phase1(BaseModel):
    # kra: FormBase
    # target: FormBase
    # resource_required: FormBase
    status:bool




class get_Phase1(BaseModel):
    kra: FormBase
    target: FormBase
    resource_required: FormBase

