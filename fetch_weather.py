import requests
import json
from datetime import datetime
import os

# Configuration for Athens, GA
LAT = 33.941993
LON = -83.375814

def fetch_weather():
    print(f"[{datetime.now()}] Fetching weather data for Athens, GA...")
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": ["temperature_2m", "shortwave_radiation", "direct_normal_irradiance", "wind_speed_80m", "relative_humidity_2m"],
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",
        "forecast_days": 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Save to a JSON file
    filename = 'daily_weather_athens.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    fetch_weather()
