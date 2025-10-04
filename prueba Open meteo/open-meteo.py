import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import numpy as np
from datetime import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

def obtener_datos_meteorologicos(latitud, longitud, fecha_inicio, fecha_fin):
    
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "shortwave_radiation_sum",
        "hourly": [
            "temperature_2m", "relativehumidity_2m", "precipitation",
            "pressure_msl", "windspeed_10m", "winddirection_10m",
            "boundary_layer_height", "shortwave_radiation"
        ],
        "timezone": "auto",
        "start_date": fecha_inicio,
        "end_date": fecha_fin
    }
    responses = openmeteo.weather_api(url, params=params)
    
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
    
    # Process hourly data. The order of variables needs to be the same as requested.
    
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_boundary_layer_height = hourly.Variables(6).ValuesAsNumpy()
    
    hourly_data = { "date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["boundary_layer_height"] = hourly_boundary_layer_height
    
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print("\nHourly data\n", hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    
    daily = response.Daily()
    daily_shortwave_radiation_sum = daily.Variables(0).ValuesAsNumpy()
    
    daily_data = { "date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
    
    daily_dataframe = pd.DataFrame(data=daily_data)

    print("\nDaily data\n", daily_dataframe)
    
    # exit the function
    return

print(obtener_datos_meteorologicos( 19.43, -99.13, "2024-01-01", "2024-02-01"))


# 18.054575989114205, -92.93761224762567

# 19.43, -99.13

# 17.99421, -180