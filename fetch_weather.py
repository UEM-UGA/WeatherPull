import requests
import pandas as pd
from datetime import datetime, timedelta
import os

LAT, LON = 33.941993, -83.375814
FOLDER = 'daily_data'

def fetch_and_save():
    target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    filename = f"{FOLDER}/weather_{target_date}.csv"
    
    # Ensure folder exists
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT, "longitude": LON,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
                   "shortwave_radiation", "direct_normal_irradiance", "diffuse_radiation", 
                   "cloud_cover", "wind_speed_80m", "surface_pressure"],
        "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
        "timezone": "America/New_York", "past_days": 1, "forecast_days": 0
    }

    try:
        print(f"[*] Fetching: {target_date}")
        response = requests.get(url, params=params)
        print(f"      Response: {response.status_code}")
        response.raise_for_status()
        
        df = pd.DataFrame(response.json()['hourly'])
        df.dropna(inplace=True) # Remove NaNs
        
        df.to_csv(filename, index=False)
        print(f"      Saved: {filename}")

    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
