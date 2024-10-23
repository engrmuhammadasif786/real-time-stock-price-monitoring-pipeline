from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, stddev
from pyspark.sql.window import Window
from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from pyspark.sql.types import StructType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("StockPriceProcessor") \
    .getOrCreate()

# MongoDB client
client = MongoClient('mongodb://mongodb:27017/')
db = client['stock_db']
collection = db['stock_data']

# Kafka consumer setup
consumer = KafkaConsumer('stock_prices', bootstrap_servers=['kafka:9092'])

def parse_stock_data(stock_data):
    time_series = stock_data.get("Time Series (1min)", {})
    rows = []
    
    for timestamp, values in time_series.items():
        rows.append({
            "timestamp": timestamp,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })
    
    return rows

for msg in consumer:
    stock_data = json.loads(msg.value)
    rows = parse_stock_data(stock_data)
    if len(rows)==0:
        continue
    df = spark.createDataFrame(rows)
    
    # Calculate rolling averages (e.g., 10 and 30 periods)
    windowSpec = Window.orderBy("timestamp").rowsBetween(-10, 0)
    df = df.withColumn("rolling_avg_10", avg(col("close")).over(windowSpec))
    
    windowSpec = Window.orderBy("timestamp").rowsBetween(-30, 0)
    df = df.withColumn("rolling_avg_30", avg(col("close")).over(windowSpec))

    # Calculate volatility (standard deviation of the price)
    df = df.withColumn("volatility", stddev(col("close")).over(windowSpec))

    # Write to MongoDB
    try:
        records = df.toJSON().map(lambda j: json.loads(j)).collect()
        if records:
            collection.insert_many(records)
        else:
            print("No records to insert")
    except Exception as e:
        print(f"Error while inserting records into MongoDB: {e}")

