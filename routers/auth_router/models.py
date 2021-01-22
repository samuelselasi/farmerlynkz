from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime, time, timedelta
from sqlalchemy.orm import relationship
from fastapi import Body, FastAPI
from typing import Optional
from database import Base
from uuid import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class AdminDeadline(Base):
    __tablename__ = "deadline"
    
    id = Column(Integer, primary_key=True, index=True)
    deadline_type = Column(String, index=True)
    start_date = str(datetime)
    end_date = str(datetime)


