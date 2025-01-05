import os
import requests
import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

# Function to get weather data from OpenWeatherMap API
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Custom filter to format timestamp
@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        data = get_weather(city)
        return render_template('index.html', data=data)
    return render_template('index.html')

@app.route("/health")
def health():
    return jsonify(status="UP")

@app.route("/weather/<city>")
def weather(city: str):
    data = get_weather(city)
    return render_template('weather.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
