from sqlalchemy.orm import Session

from . import models, schemas

from fastapi import Depends


async def read_appraiser_appraisees(user_id, db: Session):
    res = db.execute(""" select get_list_of_appraisee(:user_id) """,{'user_id':user_id})
    return res.fetchall()