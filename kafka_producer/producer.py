from kafka import KafkaProducer
import requests
import json
import time

API_KEY = 'LAJQK6IKUG950JBO'
STOCK_SYMBOL = 'AAPL'
KAFKA_TOPIC = 'stock_prices'
KAFKA_SERVER = 'kafka:9092'  

def get_stock_price():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}&interval=1min&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                        api_version=(0,11,5),
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    stock_data = get_stock_price()
    producer.send(KAFKA_TOPIC, stock_data)
    time.sleep(60)  # Fetch every 60 seconds
