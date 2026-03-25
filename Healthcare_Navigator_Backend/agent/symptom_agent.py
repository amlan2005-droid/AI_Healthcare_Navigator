from services.chat_service import generate_chat_response

def symptom_agent(session_id, message):

    prompt = f"""
    You are a medical symptom assistant.

    User symptom:
    {message}

    Explain possible causes and suggest precautions.
    """

    return generate_chat_response(session_id, prompt)