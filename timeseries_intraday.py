import requests
from flask import Flask, render_template
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    symbol = "AAPL"
    interval = "1min"
    apikey = os.getenv("API_KEY")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={apikey}"
    response = requests.get(url)
    data = response.json()

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
