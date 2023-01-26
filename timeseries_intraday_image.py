import requests
import mplcursors
from flask import Flask, render_template
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from io import BytesIO
import base64

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    # Specify the stock symbol and interval for the intraday data
    symbol = "AAPL"
    interval = "1min"
    apikey = os.getenv("API_KEY")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={apikey}"
    response = requests.get(url)
    data = response.json()

   # Extract the time series data from the JSON response
    time_series = data["Time Series (1min)"]

    # Convert the time series data to a pandas DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')

    # Convert the timestamp strings to datetime objects
    df.index = pd.to_datetime(df.index)

    fig, ax = plt.subplots()
    ax.plot(df.index, df["4. close"])
    ax.xaxis.set_major_formatter(mdates.DateFormatter(' %H:%M'))


    # Plot the closing price of the stock
    # names of columns: 1. open   2. high    3. low  4. close  5. volume
    # plt.plot(df["4. close"])
    plt.xlabel("Time")
    plt.ylabel("Closing Price")
    plt.title(f"{symbol} Intraday Stock Price")    
    plt.xticks(rotation=45)
    # Save the plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the plot as a base64 string
    plot_url = base64.b64encode(buf.getvalue()).decode()

    return render_template("index_image.html", plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
