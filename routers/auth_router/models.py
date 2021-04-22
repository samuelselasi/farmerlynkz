from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from database import Base, SessionLocal
from ..user_router.models import User
import datetime, utils

class ResetPasswordCodes(Base):
    __tablename__ = 'reset_password_codes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True)
    user_id = Column(Integer, unique=True)
    user_email = Column(String, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @staticmethod
    def generate_code():
        return utils.gen_alphanumeric_code(16)
class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
