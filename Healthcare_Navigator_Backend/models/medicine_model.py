from sqlalchemy import Column, Integer, String, Float, Text
from database.db import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    generic_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    pharmacy = Column(String, nullable=True)
    price = Column(Float, nullable=True)