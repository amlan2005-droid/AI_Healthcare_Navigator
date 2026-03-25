from rapidfuzz import process, fuzz
from database.db import SessionLocal
from models.medicine_model import Medicine
from utils.text_cleaner import normalize_name


def get_all_medicines() -> list[str]:
    """Fetch all medicine names from DB (normalized)."""
    session = SessionLocal()
    try:
        meds = session.query(Medicine.name).all()
        # Ensure we normalize DB entries for more accurate matching
        return [normalize_name(m[0]) for m in meds if m[0]]
    finally:
        session.close()


def find_closest_medicine(query: str, choices: list[str]):
    """Match medicine with fuzzy logic and assign confidence."""
    if not query:
        return None, 0, "low"

    # Get top 3 matches to evaluate ambiguity
    matches = process.extract(query, choices, scorer=fuzz.WRatio, limit=3)
    
    if not matches:
        return None, 0, "low"

    best = matches[0]
    
    # Handle single match case
    if len(matches) == 1:
        if best[1] >= 90:
            return best[0], best[1], "high"
        elif best[1] >= 75:
            return best[0], best[1], "medium"
        return best[0], best[1], "low"

    second = matches[1]

    # 🧠 FIRST: ambiguity check (Ambiguity > Score)
    # If the gap between top two matches is small (< 5), it's uncertain
    if best[1] - second[1] < 10:  # Increased ambiguity margin
        return best[0], best[1], "medium"

    # 🧠 THEN: confidence check based on score
    if best[1] >= 90:
        return best[0], best[1], "high"
    elif best[1] >= 75:
        return best[0], best[1], "medium"
        
    return best[0], best[1], "low"


def get_medicine_info(medicines: list[str]) -> str:
    """Return a human-readable summary of identified medicines."""
    if not medicines:
        return "No clear medicines identified."

    all_db_meds = get_all_medicines()
    results = []

    for med in medicines:
        # Normalize extracted medicine BEFORE matching
        norm_med = normalize_name(med)
        if not norm_med:
            continue

        name, score, conf = find_closest_medicine(norm_med, all_db_meds)
        
        if conf in ["high", "medium"]:
            results.append(f"{name.title()} ({conf} match)")
        else:
            # Fallback to the original extracted name if match is weak
            results.append(f"{med.title()} (unverified)")

    return ", ".join(results) if results else "No valid medicines identified."
