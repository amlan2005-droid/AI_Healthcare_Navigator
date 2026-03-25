from sqlalchemy import Column, Integer, String, Text
from database.db import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text)
    ai_reply = Column(Text)