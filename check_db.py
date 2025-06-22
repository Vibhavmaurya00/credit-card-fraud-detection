import sqlite3

conn = sqlite3.connect("fraud_detection.db")
rows = conn.execute("SELECT * FROM fraud_transactions").fetchall()

print("📄 Total frauds in DB:", len(rows))

for row in rows:
    print(row)

conn.close()
