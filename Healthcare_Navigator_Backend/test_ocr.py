from pypdf import PdfReader
import easyocr
import os

# initialize OCR once
reader = easyocr.Reader(['en'])


def extract_text(file_path: str):

    # check file type
    ext = os.path.splitext(file_path)[1].lower()

    #  PDF case
    if ext == ".pdf":
        text = ""
        pdf = PdfReader(file_path)

        for page in pdf.pages:
            text += page.extract_text() or ""

        return text

    #  Image case
    elif ext in [".png", ".jpg", ".jpeg"]:
        result = reader.readtext(file_path)
        text = " ".join([item[1] for item in result])
        return text

    else:
        return "Unsupported file type"

image_path = r"c:\Users\DELL\AI_Healthcare_Navigator\Healthcare_Navigator_Backend\venv\Lib\site-packages\skimage\data\text.png"
result = reader.readtext(image_path, detail=0)
print("OCR RAW:", result)
