from sqlalchemy import Column, Integer, String, Text
from database.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    extracted_text = Column(Text)