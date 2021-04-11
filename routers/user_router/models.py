from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, backref
from passlib.hash import pbkdf2_sha256 as sha256
from database import Base, SessionLocal
import datetime
import secrets


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    user_info=relationship('UserInfo', backref='user',uselist=False, cascade=("all, delete"))
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=True )
    

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id") ,nullable=False, unique=True)

    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    # phone = Column(String, nullable=True)
    # image_url = Column(String, nullable=True)
    # is_verified = Column(Boolean,nullable=False)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
class ResetPasswordToken(Base):
    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id") , unique=True)
    token = Column(String, index=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def generate_token():
        token = secrets.token_urlsafe(4)
        return sha256.hash(token)

    @staticmethod
    def verify_token(token, hash):
        return sha256.verify(token, hash)
class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)

    users = relationship('User', backref="user_type")

@event.listens_for(UserType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ UserType(title='System Admin'), UserType(title='Appraiser'), UserType(title='HR Manager') ])
    db.commit()