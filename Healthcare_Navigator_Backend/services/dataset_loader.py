import pandas as pd
import re
import os

# Regex patterns for cleaning
pattern_brackets = re.compile(r"\(.*?\)")
pattern_dosage = re.compile(r"\b\d+(\.\d+)?\s?(mg|ml|iu|mcg|%)\b")

# Words to ignore
NOISE_WORDS = {
    "tablet", "tablets", "capsule", "capsules", "syrup",
    "injection", "cream", "ointment", "gel", "drop", "eye",
    "ear", "soft", "gelatin", "plus", "sr", "od", "neo"
}

MIN_LENGTH = 4

def clean_text(text):
    if not isinstance(text, str):
        return []
        
    text = text.lower()
    
    # Apply regex removals
    text = pattern_brackets.sub("", text)
    text = pattern_dosage.sub("", text)
    
    # Remove special characters and numbers
    text = re.sub(r"[^a-z\s\-]", " ", text)
    
    words = text.split()
    
    cleaned = []
    for w in words:
        if w in NOISE_WORDS:
            continue
        if len(w) < MIN_LENGTH:
            continue
        if w in {"gargle", "water", "solution"}:  # extra noise identified in notebook
            continue
        cleaned.append(w)
    
    return cleaned

def get_all_medicines():
    # Use relative path from the perspective of this script or the main execution point
    # Since uvicorn runs in Healthcare_Navigator_Backend, the path "dataset/medicine_data.csv" should work
    csv_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "medicine_data.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    df = df[["product_name", "salt_composition"]]
    df.dropna(inplace=True)
    
    all_words = []
    for _, row in df.iterrows():
        all_words.extend(clean_text(row["product_name"]))
        all_words.extend(clean_text(row["salt_composition"]))
    
    # Remove duplicates
    all_words = sorted(list(set(all_words)))
    
    return all_words

# For backward compatibility with the user's initial script idea
all_words = get_all_medicines() if __name__ == "__main__" or os.getenv("SEEDING") else []
