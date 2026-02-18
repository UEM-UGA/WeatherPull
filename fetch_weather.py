import requests
import pandas as pd
from datetime import datetime, timedelta
import os

FILENAME = 'daily_weather_athens.csv'
LAT, LON = 33.941993, -83.375814

def fetch_rich_data():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Expanded variable list for Energy Engineering
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "dew_point_2m", 
            "apparent_temperature", "shortwave_radiation", "direct_normal_irradiance", 
            "diffuse_radiation", "cloud_cover", "wind_speed_80m", "surface_pressure"
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "America/New_York",
        "past_days": 1,
        "forecast_days": 0
    }
    
    response = requests.get(url, params=params)
    new_df = pd.DataFrame(response.json()['hourly'])

    if not os.path.exists(FILENAME):
        new_df.to_csv(FILENAME, index=False)
    else:
        existing_df = pd.read_csv(FILENAME)
        if yesterday not in existing_df['time'].values:
            new_df.to_csv(FILENAME, mode='a', index=False, header=False)
            print(f"Rich data appended for {yesterday}")

if __name__ == "__main__":
    fetch_rich_data()
