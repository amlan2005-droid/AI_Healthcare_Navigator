import uuid
from fastapi import APIRouter
from schemas.session_schema import SessionResponse

router = APIRouter()

@router.post("/session", response_model=SessionResponse)
def create_session():

    session_id = str(uuid.uuid4())

    return {"session_id": session_id}