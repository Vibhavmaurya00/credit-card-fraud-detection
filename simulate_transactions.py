from kafka import KafkaProducer
import json
import time
import random
from faker import Faker

fake = Faker()

# Step 1: Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("✅ Connected to Kafka and sending transactions...")

# Step 2: Loop and send transactions
while True:
    # Alternate between fraud and normal every other message
    is_fraud = 1 if random.random() < 0.5 else 0  # 50% fraud rate

    transaction = {
        "card_id": fake.credit_card_number(),
        "amount": round(random.uniform(1.0, 1000.0), 2),
        "timestamp": fake.iso8601(),
        "location": fake.city(),
        "merchant": fake.company(),
        "is_fraud": is_fraud
    }

    producer.send('transactions', transaction)
    print("🚀 Sent transaction:", transaction)
    time.sleep(1)



