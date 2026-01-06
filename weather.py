from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv() 

API_KEY = os.getenv("API_key")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')


@weather_bp.route('/')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify ({"error": "City parameter is required"}), 400
    
    prams = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        'lang': 'ru'
    }

    try:
        response = requests.get(BASE_URL, params=prams, timeout=5)
        response.raise_for_status()

        data = response.json()

        weather_info = {
            "city": data.get("name"),
            "temperature": data["main"].get("temp"),
            "description": data["weather"][0].get("description"),
            "humidity": data["main"].get("humidity"),
            "wind_speed": data["wind"].get("speed"),
            "timestamp": datetime.utcfromtimestamp(data.get("dt")).strftime('%Y-%m-%d %H:%M:%S')
        }    

        return jsonify(weather_info)
    except requests.exceptions.HTTPError:
        return jsonify({"error": "City not found"}), 404
    except requests.exceptions.RequestException:
        return jsonify({"error": "Error fetching data from weather service"}), 500
    
@weather_bp.route("/temp")
def temperature():
    city = request.args.get("city")
    return {"city": city, "temp": "soon"}
