import psycopg2
import os
from dotenv import load_dotenv
from dataset_loader import get_all_medicines
from utils.text_cleaner import normalize_name

# Load environment variables from .env
load_dotenv()

# Database connection details from .env
DB_NAME = "ai_healthcare_db"
DB_USER = "postgres"
DB_PASS = "am2005"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    print("Loading medicine dataset...")
    all_words = get_all_medicines()
    print(f"Total unique medicines found (raw): {len(all_words)}")

    print("Connecting to database...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    
    cur = conn.cursor()

    insert_query = """
    INSERT INTO medicines (name)
    VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
    """

    print("Normalizing and inserting medicines into database...")
    count = 0
    for med in all_words:
        # Step 2: Normalize before matching/storing
        normalized = normalize_name(med)
        
        # ⚠️ Relaxed filtering as per user instructions:
        # Keep DB as complete as possible, only filter extremely short noise.
        if len(normalized) > 3:
            cur.execute(insert_query, (normalized,))
            count += 1

    conn.commit()
    print(f"Successfully processed and seeded {count} medicines!")

    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")