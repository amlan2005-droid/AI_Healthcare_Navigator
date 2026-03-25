from pypdf import PdfReader
import easyocr
import os
import cv2
from PIL import Image
from utils.text_cleaner import clean_extracted_text, normalize_name

# initialize OCR once
reader = easyocr.Reader(['en'])

# ---------------- IMAGE PREPROCESSING ---------------- #

def preprocess_image(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Increase contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # 2. Denoise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 3. Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15,
        C=10
    )

    # 4. Morphological opening
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return thresh

# ---------------- MAIN FUNCTION ---------------- #

def extract_text(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    # -------- PDF -------- #
    if ext == ".pdf":
        text = ""
        pdf = PdfReader(file_path)

        for page in pdf.pages:
            text += page.extract_text() or ""

        cleaned = clean_extracted_text(text)
        return {
            "raw_text": cleaned
        }

    # -------- IMAGE -------- #
    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        # Convert webp → jpg if needed
        if ext == ".webp":
            img = Image.open(file_path).convert("RGB")
            file_path = "temp.jpg"
            img.save(file_path)

        processed_img = preprocess_image(file_path)
        if processed_img is None:
            return {"error": "Could not read image file."}

        result = reader.readtext(processed_img, detail=1)

        extracted_words = []
        for (bbox, text_val, prob) in result:
            if prob > 0.4:  # slightly lower threshold for better recall
                extracted_words.append(text_val)

        text = " ".join(extracted_words)
        cleaned = clean_extracted_text(text)

        # 🚨 reject bad OCR
        if len(cleaned) < 10:
            return {
                "error": "Low quality image. Please upload a clearer prescription."
            }

        return {
            "raw_text": cleaned
        }

    else:
        return {"error": "Unsupported file type"}
