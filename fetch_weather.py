import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIG ---
LAT, LON = 33.941993, -83.375814
FILENAME = 'daily_weather_athens.csv'

def fetch_and_clean():
    target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"[*] Cloud Fetch Start: {target_date}")

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
        print(f"[1/3] Requesting API...")
        response = requests.get(url, params=params)
        print(f"      Response: {response.status_code}")
        response.raise_for_status()
        
        print("[2/3] Cleaning Data (Removing NaNs)...")
        df = pd.DataFrame(response.json()['hourly'])
        df.dropna(inplace=True) 
        
        print(f"[3/3] Saving to {FILENAME}...")
        df.to_csv(FILENAME, index=False)
        print("      Success.")

    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_clean()
