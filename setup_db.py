import sqlite3

conn = sqlite3.connect("fraud_detection.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS fraud_transactions (
    card_id TEXT,
    amount REAL,
    timestamp TEXT,
    location TEXT,
    merchant TEXT
)
""")

conn.commit()
conn.close()
print("✅ Table created successfully!")

