import logging
import google.generativeai as genai
from config import settings

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

# Use the working model we found earlier
model = genai.GenerativeModel("gemini-2.5-flash")

def route_query(user_message: str):
    prompt = f"""
    You are a healthcare triage AI.

    Decide which agent should handle the user's request.

    Available agents:
    - symptom_agent
    - medicine_agent
    - doctor_agent

    Return ONLY the agent name.
    Do not explain.

    User message:
    {user_message}
    """

    try:
        response = model.generate_content(prompt)
        decision = response.text.strip().lower()
        
        logger.info("User message: %s", user_message)
        logger.info("Selected agent: %s", decision)
        
        return decision
    except Exception as e:
        logger.error("Routing error: %s", str(e))
        # Fallback to symptom agent if LLM fails
        return "symptom_agent"