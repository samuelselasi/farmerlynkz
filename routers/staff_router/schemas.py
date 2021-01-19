from typing import List, Optional

from pydantic import BaseModel





class staffBase(BaseModel):
    title: str
    description: Optional[str] = None



class staffCreate(staffBase):
    pass



class staff(staffBase):
    id: int
