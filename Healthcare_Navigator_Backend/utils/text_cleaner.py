import re

CHEMICAL_SUFFIXES = (
    "ine", "ol", "ide", "ate", "ium", "cin", "mab", "vir", "zole"
)

IGNORE_WORDS = {
    # Template/form labels
    "name", "surname", "registration", "address", "department", "date", "stamp", "checked",
    "prescription", "form", "unit",
    # Doctor / clinic info
    "doctor", "postal", "akuh", "clinic", "hospital", "signature", "patient", "dispensed",
    # Dosage instructions / noise
    "morning", "night", "daily", "meals", "after", "before", "times", "days", "week", "month", 
    "dose", "tablet", "tablets", "capsule", "capsules", "syrup", "injection", "cream", 
    "ointment", "gel", "drop", "eye", "ear", "soft", "gelatin", "plus", "sr", "od", "neo",
    "gargle", "water", "solution", "follow"
}

def normalize_name(name: str) -> str:
    """Standardize medicine name for better matching."""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r"\(.*?\)", "", name)   # remove brackets
    name = re.sub(r"\d+mg|\d+ml|\d+iu|\d+mcg|\d+%", "", name)     # remove dosage
    name = re.sub(r"[^a-z\s\-]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def is_valid_medicine(word: str) -> bool:
    """Filter out noise, allowing legitimate medicine names."""
    w = word.strip().lower()

    # ❌ too short
    if len(w) <= 3:
        return False

    # ❌ common noise words
    if w in IGNORE_WORDS:
        return False

    # ❌ contains digits (dosage etc)
    if any(ch.isdigit() for ch in w):
        return False

    # ❌ junk characters
    if not w.replace("-", "").isalpha():
        return False

    # ✅ RELAXED chemical-like filter: only remove if very long
    if len(w) > 12 and any(w.endswith(suffix) for suffix in CHEMICAL_SUFFIXES):
        return False

    return True

def clean_extracted_text(text: str) -> str:
    """Clean raw OCR text by removing known noise words."""
    words = text.split()
    filtered = [w for w in words if w.lower() not in IGNORE_WORDS]
    return " ".join(filtered)
