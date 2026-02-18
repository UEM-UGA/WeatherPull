import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIG ---
LAT, LON = 33.941993, -83.375814
FILENAME = 'daily_weather_athens.csv'

def fetch_and_clean():
    # 1. Target Yesterday
    target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"[*] Starting Cloud Fetch for: {target_date}")

    # 2. API Request
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
        print(f"[1/3] Requesting data from Open-Meteo...")
        response = requests.get(url, params=params)
        print(f"      Server Response: {response.status_code}")
        response.raise_for_status()
        
        # 3. Clean Data (Remove NaN)
        print("[2/3] Cleaning data (Removing NaN/Nulls)...")
        df = pd.DataFrame(response.json()['hourly'])
        df.dropna(inplace=True) # Removes any rows with missing data
        
        # 4. Save
        print(f"[3/3] Saving to {FILENAME}...")
        df.to_csv(FILENAME, index=False)
        print("      Success.")

    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_clean()
