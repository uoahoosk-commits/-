"""
Weather Data Collection Module
Collects historical daily maximum temperature data for Seoul using Open-Meteo API
"""

import requests
import pandas as pd
from datetime import datetime, timedelta


def collect_weather_data():
    """
    Collects 1 year of daily maximum temperature data for Seoul
    using the Open-Meteo API (latitude: 37.5665, longitude: 126.9780)
    Saves the result to weather.csv
    """
    
    # API configuration
    latitude = 37.5665
    longitude = 126.9780
    
    # Calculate date range (past 1 year from today)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    # Open-Meteo API endpoint
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_max",
        "timezone": "Asia/Seoul"
    }
    
    try:
        print(f"Fetching weather data from {start_date} to {end_date}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract data
        dates = data["daily"]["time"]
        temps = data["daily"]["temperature_2m_max"]
        
        # Create DataFrame
        df = pd.DataFrame({
            "date": dates,
            "max_temp": temps
        })
        
        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
        
        # Save to CSV
        df.to_csv("weather.csv", index=False, encoding="utf-8")
        
        print(f"✓ Data saved to weather.csv")
        print(f"  - Total records: {len(df)}")
        print(f"  - Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"  - Temperature range: {df['max_temp'].min()}°C to {df['max_temp'].max()}°C")
        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data from API: {e}")
        return None
    except Exception as e:
        print(f"✗ Error processing data: {e}")
        return None


if __name__ == "__main__":
    collect_weather_data()
