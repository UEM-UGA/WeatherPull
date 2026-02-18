import requests
import pandas as pd
from datetime import datetime, timedelta
import os

LAT, LON = 33.941993, -83.375814
FOLDER = 'daily_data'

def fetch_and_save():
    # 1. Create the date-based filename
    target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    filename = f"{FOLDER}/weather_{target_date}.csv"
    
    print(f"[*] Target: {target_date}")

    # 2. Ensure the folder exists on the GitHub runner
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
        print(f"[*] Created folder: {FOLDER}")

    # 3. Request Weather Data
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
        print(f"[1/3] Fetching data...")
        response = requests.get(url, params=params)
        print(f"      Server: {response.status_code}")
        response.raise_for_status()
        
        print("[2/3] Cleaning data...")
        df = pd.DataFrame(response.json()['hourly'])
        df.dropna(inplace=True) # Remove nulls
        
        print(f"[3/3] Saving: {filename}")
        df.to_csv(filename, index=False)
        print("      Success.")

    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
