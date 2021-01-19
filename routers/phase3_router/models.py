from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from database import Base



class phase1(Base):
    __tablename__ = "phase1"

    id = Column(Integer, primary_key=True, index=True)
    kra = Column(String, index=True)
    target = Column(String, index=True)
    resource_required = Column(String, index=True)
    status = Column(Boolean, default=True)