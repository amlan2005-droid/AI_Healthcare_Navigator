import os
from services.text_extractor import extract_text
from services.trocr_extractor import extract_text_trocr
from services.medicine_retriever import get_all_medicines, find_closest_medicine
from utils.text_cleaner import is_valid_medicine, normalize_name

def extract_candidates_from_text(text: str) -> list[str]:
    """Extract potential medicine names using regex and stopwords."""
    import re
    if not text:
        return []

    text = text.lower()
    # Find all lowercase words with at least 3 characters
    words = re.findall(r"[a-z]{3,}", text)

    stopwords = {
        "tab", "tablet", "cap", "capsule",
        "mg", "ml", "tds", "bd", "od", "hs",
        "morning", "night", "nite", "after", "before", "food"
    }

    candidates = []
    for w in words:
        if w in stopwords:
            continue
        # Controlled filtering by length
        if len(w) < 4 or len(w) > 12:
            continue
        candidates.append(w)

    return list(set(candidates))

def prescription_agent(file_path: str, session_id: str = None) -> dict:
    """Analyze a prescription image/PDF and return identified medicines."""
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    #  OCR SELECTION: 
    # Use TrOCR for images (handwriting), use pypdf for PDF files
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        print(f"DEBUG: Using TrOCR for {filename}...")
        extraction_result = extract_text_trocr(file_path)
        
        # Fallback to easyocr if TrOCR fails
        if "error" in extraction_result:
            print(f"DEBUG: TrOCR failed ({extraction_result['error']}), falling back to easyocr...")
            extraction_result = extract_text(file_path)
    else:
        # PDFs still use pypdf
        extraction_result = extract_text(file_path)

    # Handle bad OCR / unreadable files
    if "error" in extraction_result:
        return {"filename": filename, "analysis": extraction_result["error"]}

    text = extraction_result.get("raw_text", "")
    print(f"DEBUG: Raw OCR Text: '{text}'")  # 🔍 Trace what actually came back

    if not text:
        return {"filename": filename, "analysis": "No readable text found."}

    # Extract raw candidates and clean them
    raw_candidates = extract_candidates_from_text(text)
    
    # Filter and normalize candidates
    candidates = []
    for cand in raw_candidates:
        norm = normalize_name(cand)
        if is_valid_medicine(norm):
            candidates.append(norm)

    print("\n===== DEBUG PIPELINE =====")
    print("OCR TEXT:\n", text)
    print("RAW CANDIDATES:\n", raw_candidates)
    print("FILTERED CANDIDATES:\n", candidates)

    if not candidates:
        print("FINAL MATCHES: []")
        print("=========================\n")
        return {
            "filename": filename,
            "analysis": {
                "medicines": [],
                "warning": "OCR text unclear. Try better image or preprocessing."
            }
        }

    # Fetch DB medicines
    medicine_db = get_all_medicines()
    if not medicine_db:
        return {"filename": filename, "analysis": "Medicine database is empty."}

    # Fuzzy match candidates
    matched_meds = []
    seen = set()
    for cand in candidates:
        name, score, confidence = find_closest_medicine(cand, medicine_db)
        
        # 🧠 ONLY accept top-tier matches (Score >= 90)
        if confidence != "high":
            continue

        if name not in seen:
            seen.add(name)
            matched_meds.append({
                "name": name.title(),
                "confidence": confidence,
                "score": score
            })

    if not matched_meds:
        return {"filename": filename, "analysis": "No medicines matched in database."}

    # Sort by score descending and take top 3
    matched_meds = sorted(matched_meds, key=lambda x: x["score"], reverse=True)
    matched_meds = matched_meds[:3]

    print("FINAL MATCHES:\n", [m["name"] for m in matched_meds])
    print("=========================\n")

    warning = ""
    if any(m["confidence"] == "medium" for m in matched_meds):
        warning = "Some medicines have medium detection confidence — please verify."

    return {
        "filename": filename,
        "analysis": {
            "medicines": matched_meds,
            "warning": warning
        }
    }