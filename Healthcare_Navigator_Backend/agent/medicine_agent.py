from services.chat_service import generate_chat_response

def medicine_agent(session_id, message):

    prompt = f"""
    You are a medicine information assistant.

    Question:
    {message}

    Explain the medicine, uses, and precautions.
    """

    return generate_chat_response(session_id, prompt)