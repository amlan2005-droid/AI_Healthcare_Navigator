from fastapi import APIRouter, UploadFile, File
import os
import shutil

from agent.prescription_agent import prescription_agent

router = APIRouter()

UPLOAD_FOLDER = "uploads"

@router.post("/analyze-prescription")
async def analyze_prescription(file: UploadFile = File(...)):

    # ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # run prescription agent
    result = prescription_agent(file_path)

    return result