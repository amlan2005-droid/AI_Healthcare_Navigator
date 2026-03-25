from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Healthcare Navigator"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/ai_healthcare_db"
    )

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()