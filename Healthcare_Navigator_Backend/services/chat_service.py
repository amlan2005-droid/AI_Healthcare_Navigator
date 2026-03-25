import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

chat_memory = {}

def generate_chat_response(session_id: str, user_message: str):

    try:

        if session_id not in chat_memory:
            chat_memory[session_id] = []

        chat_memory[session_id].append(
            {"role": "user", "content": user_message}
        )

        history_text = ""

        for msg in chat_memory[session_id]:
            history_text += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
        You are a healthcare assistant AI.

        Conversation history:
        {history_text}

        Assistant:
        """

        response = model.generate_content(prompt)

        reply = response.text

        chat_memory[session_id].append(
            {"role": "assistant", "content": reply}
        )

        return reply

    except Exception as e:
        import traceback
        return f"AI error traces: {str(e)} - {traceback.format_exc()}"