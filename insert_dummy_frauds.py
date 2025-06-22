import sqlite3
from faker import Faker
import random

fake = Faker()

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

# Insert 5 fake fraud rows
for _ in range(5):
    cursor.execute("""
        INSERT INTO fraud_transactions (card_id, amount, timestamp, location, merchant)
        VALUES (?, ?, ?, ?, ?)
    """, (
        fake.credit_card_number(),
        round(random.uniform(100.0, 1000.0), 2),
        fake.iso8601(),
        fake.city(),
        fake.company()
    ))

conn.commit()
conn.close()

print("✅ Inserted 5 fake frauds into fraud_detection.db")
