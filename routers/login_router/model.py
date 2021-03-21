from sqlalchemy import String
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import Column
from .login_db import Base


class User_list(Base):
    __tablename__ = 'user_list'

    email = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
