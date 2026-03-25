import re
from pypdf import PdfReader

def extract_medicines(text):

    pattern = r'\b[A-Z][a-zA-Z]+\b'

    medicines = re.findall(pattern, text)

    return medicines

def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text