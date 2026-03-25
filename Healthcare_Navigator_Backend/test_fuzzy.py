import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from services.medicine_retriever import find_closest_medicine

choices = ["amoxicillin", "paracetamol", "ibuprofen", "aspirin"]

test_cases = [
    ("Amoxicillin", "high"),
    ("Amoxicil", "medium"),
    ("Paracetam", "medium"),
    ("Para", "low"),
    ("Ibu", "low"),
]

print("Testing find_closest_medicine...")
for query, expected_conf in test_cases:
    name, score, conf = find_closest_medicine(query.lower(), choices)
    print(f"Query: {query} -> Match: {name} (Score: {score}, Confidence: {conf})")
