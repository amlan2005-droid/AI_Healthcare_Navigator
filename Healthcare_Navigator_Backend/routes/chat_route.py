from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.chat_schema import ChatRequest, ChatResponse
from services.chat_service import generate_chat_response
from database.db import get_db
from models.chat_model import ChatHistory

from agent.triage_agent import route_query
from agent.symptom_agent import symptom_agent
from agent.medicine_agent import medicine_agent
from agent.doctor_agent import doctor_agent
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):

    session_id = request.session_id or str(uuid.uuid4())

    agent = route_query(request.message)

    if "medicine" in agent:
        ai_reply = medicine_agent(session_id, request.message)
    elif "doctor" in agent:
        ai_reply = doctor_agent(session_id, request.message)
    else:
        ai_reply = symptom_agent(session_id, request.message)

    chat = ChatHistory(
        user_message=request.message,
        ai_reply=ai_reply
    )

    db.add(chat)
    db.commit()

    return ChatResponse(reply=ai_reply, session_id=session_id)