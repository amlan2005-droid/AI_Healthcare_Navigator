from database.db import engine, Base

# Import all models so SQLAlchemy knows them
from models.user_model import User
from models.chat_model import ChatHistory
from models.prescription_model import Prescription
from models.doctor_model import Doctor
from models.medicine_model import Medicine


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()