from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from routes.session_routes import router as session_router


from config import settings
from database.db import get_db

# Import routes
from routes.chat_route import router as chat_router
from routes.prescription_routes import router as prescription_router
from routes.doctor_routes import router as doctor_router
from routes.medicine_route import router as medicine_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Healthcare Navigator API"
)

# CORS Configuration
origins = ["*"]  # Allow all origins for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routers
app.include_router(chat_router, prefix="/api")
app.include_router(prescription_router, prefix="/api")
app.include_router(doctor_router, prefix="/api")
app.include_router(medicine_router, prefix="/api")

app.include_router(session_router, prefix="/api")
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    return {"database_connection": result[0]}

@app.get("/")
def root():
    return {"message": "AI Healthcare Navigator API running"}
