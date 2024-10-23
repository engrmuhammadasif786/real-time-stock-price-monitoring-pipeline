import json
from flask import Flask, render_template
from pymongo import MongoClient
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client['stock_db']

@app.route('/')
def index():
    # Fetch stock data 
    stock_data = list(db['stock_data'].find().limit(100))

    # Extract data for plotting (timestamp, price, volume, rolling_avg_10, rolling_avg_30)
    timestamps = [item['timestamp'] for item in stock_data]
    prices = [item['close'] for item in stock_data]
    volumes = [item['volume'] for item in stock_data]
    rollingAvg10 = [item['rolling_avg_10'] for item in stock_data]
    rollingAvg30 = [item['rolling_avg_30'] for item in stock_data]

    # Stock price plot
    price_data = [go.Scatter(x=timestamps, y=prices, mode='lines', name='Stock Price')]
    price_json = json.dumps(price_data, cls=PlotlyJSONEncoder)

    # Volume traded plot
    volume_data = [go.Bar(x=timestamps, y=volumes, name='Volume Traded')]
    volume_json = json.dumps(volume_data, cls=PlotlyJSONEncoder)

    # 10 days rolling average
    rolling_avg_data_10 = [go.Scatter(x=timestamps, y=rollingAvg10, mode='lines', name='10-Day Moving Avg')]
    rolling_avg_json_10 = json.dumps(rolling_avg_data_10, cls=PlotlyJSONEncoder)

    # 30 days rolling average
    rolling_avg_data_30 = [go.Scatter(x=timestamps, y=rollingAvg30, mode='lines', name='30-Day Moving Avg')]
    rolling_avg_json_30 = json.dumps(rolling_avg_data_30, cls=PlotlyJSONEncoder)

    return render_template('index.html', 
                           price_data=price_json, 
                           volume_data=volume_json, 
                           rolling_avg_json_10=rolling_avg_json_10,
                           rolling_avg_json_30=rolling_avg_json_30)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
