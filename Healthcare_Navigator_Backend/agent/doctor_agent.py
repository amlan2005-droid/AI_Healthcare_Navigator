from services.chat_service import generate_chat_response

def doctor_agent(session_id, message):

    prompt = f"""
    You are a healthcare navigator.

    Based on the user's problem recommend which doctor they should visit.

    Question:
    {message}
    """

    return generate_chat_response(session_id, prompt)