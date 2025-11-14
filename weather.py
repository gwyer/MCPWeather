# weather.py
import requests

def get_weather_for_city(city):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()

    if "results" not in geo:
        return {"error": "City not found"}

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    w = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True}
    ).json()

    return w["current_weather"]
