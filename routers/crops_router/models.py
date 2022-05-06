from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime
import secrets
import string
import random

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sel@localhost:5432/farmerlynkz"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()


uppercase_and_digits = string.ascii_uppercase + string.digits
lowercase_and_digits = string.ascii_lowercase + string.digits

# GENERATE ACCESS CODES


def gen_alphanumeric_code(length):
    code = ''.join((random.choice(uppercase_and_digits)
                   for i in range(length)))
    return code


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    othernames = Column(String, index=True, nullable=True)
    phone = Column(Integer, index=True, nullable=True)
    dateofbirth = Column(DateTime, index=True)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class ResetPasswordToken(Base):
    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
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
    db.add_all([UserType(title='System Admin'), UserType(
        title='Appraiser'), UserType(title='Appraisee')])
    db.commit()


class ResetPasswordCodes(Base):
    __tablename__ = 'reset_password_codes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True)
    user_id = Column(Integer, unique=True)
    user_email = Column(String, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @staticmethod
    def generate_code():
        return gen_alphanumeric_code(32)


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
