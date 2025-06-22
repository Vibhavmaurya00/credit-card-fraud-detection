from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

# Step 1: Start Spark session
spark = SparkSession.builder \
    .appName("CreditCardFraudDetector") \
    .master("local[*]") \
    .config("spark.jars", "jars/spark-sql-kafka-0-10_2.12-3.5.1.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Step 2: Define schema
schema = StructType() \
    .add("card_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("timestamp", StringType()) \
    .add("location", StringType()) \
    .add("merchant", StringType()) \
    .add("is_fraud", IntegerType())

# Step 3: Read from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Step 4: Parse JSON
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Step 5: Filter fraud only
frauds = df_parsed.filter(col("is_fraud") == 1)

# Step 6: Save to SQLite
def save_to_sqlite(df, epoch_id):
    import sqlite3
    frauds = df.collect()
    print("🧪 Fraud rows in batch:", len(frauds))

    if len(frauds) == 0:
        return

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

    for row in frauds:
        cursor.execute("""
            INSERT INTO fraud_transactions (card_id, amount, timestamp, location, merchant)
            VALUES (?, ?, ?, ?, ?)
        """, (row['card_id'], row['amount'], row['timestamp'], row['location'], row['merchant']))

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(frauds)} fraud rows into database.")

# Step 7: Run the query
query = frauds.writeStream \
    .foreachBatch(save_to_sqlite) \
    .outputMode("append") \
    .start()

query.awaitTermination()


