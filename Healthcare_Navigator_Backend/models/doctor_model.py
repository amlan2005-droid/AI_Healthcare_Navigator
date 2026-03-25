from sqlalchemy import Column, Integer, String
from database.db import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    hospital = Column(String)
    address = Column(String)