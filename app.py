from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads .env
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

def fetch_weather(city: str):
    """Call OpenWeather API and return a small dict or (None, error)."""
    if not API_KEY:
        return None, "API key missing. Put it in .env as OPENWEATHER_API_KEY."
    if not city:
        return None, "Please enter a city name."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        # Debug tip (uncomment if needed): print(data)

        if res.status_code == 200 and "main" in data:
            return {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "country": data.get("sys", {}).get("country", "")
            }, None

        # handle common errors
        if data.get("message"):
            return None, data["message"].capitalize()

        return None, "Could not fetch weather right now."
    except requests.exceptions.RequestException:
        return None, "Network error. Check your internet and try again."

@app.route("/", methods=["GET", "POST"])
def index():
    weather, error = None, None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        weather, error = fetch_weather(city)
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    # debug=True for dev only
    app.run(debug=True)
