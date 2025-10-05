import pandas as pd
from datetime import datetime, timedelta
import os
import time
import urllib.request
import urllib.parse
import json

# --- 1. CONFIGURACIÓN ---
STATIONS = {
    "Centro_CDMX": {"lat": 19.43, "lon": -99.13, "tz_api": "auto"},
    "Centro_LA": {"lat": 34.05, "lon": -118.24, "tz_api": "America/Los_Angeles"}
}

# CAMBIO AQUÍ: Se eliminó 'pm25_prediction' de la lista de columnas
CSV_COLUMNS = [
    'timestamp', 'temperature_2m', 'relativehumidity_2m', 'precipitation', 'pressure_msl',
    'windspeed_10m', 'winddirection_10m', 'boundary_layer_height', 'shortwave_radiation_sum',
    'hour_of_day', 'day_of_week', 'month_of_year', 'is_weekend',
    'co', 'no', 'no2', 'nox', 'o3', 'pm25', 'so2'
]

HOURLY_VARS = [
    "temperature_2m", "relativehumidity_2m", "precipitation", "pressure_msl", 
    "windspeed_10m", "winddirection_10m", "boundary_layer_height"
]
DAILY_VARS = ["shortwave_radiation_sum"]

def get_api_data(lat, lon, timezone, start_date, end_date):
    """Función para llamar a la API de Open-Meteo y obtener datos horarios y diarios."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon, "timezone": timezone,
        "start_date": start_date, "end_date": end_date
    }
    hourly_params = "&".join([f"hourly={var}" for var in HOURLY_VARS])
    daily_params = "&".join([f"daily={var}" for var in DAILY_VARS])
    
    full_url = f"{base_url}?{urllib.parse.urlencode(params)}&{hourly_params}&{daily_params}"
    
    with urllib.request.urlopen(full_url) as response:
        if response.status != 200:
            raise Exception(f"La petición a la API falló con código {response.status}")
        response_body = response.read()
        return json.loads(response_body.decode("utf-8"))

# --- 2. FUNCIÓN PRINCIPAL DE CAPTURA ---
def ejecutar_captura_una_vez():
    """Realiza una única pasada de captura de datos para todas las estaciones."""
    now_utc = datetime.utcnow()
    now_cdmx = now_utc - timedelta(hours=6)
    now_la = now_cdmx - timedelta(hours=1)

    station_times = { "Centro_CDMX": now_cdmx, "Centro_LA": now_la }

    for station_name, info in STATIONS.items():
        print(f"\n--- Procesando estación: {station_name} ---")
        try:
            current_time = station_times[station_name]
            target_timestamp = current_time.replace(minute=0, second=0, microsecond=0)
            
            print(f"Hora local calculada: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Obteniendo datos para la hora: {target_timestamp.strftime('%Y-%m-%d %H:00:00')}")

            data = get_api_data(
                info["lat"], info["lon"], info["tz_api"], 
                target_timestamp.strftime('%Y-%m-%d'), 
                target_timestamp.strftime('%Y-%m-%d')
            )

            df_hourly = pd.DataFrame(data['hourly'])
            df_hourly['time'] = pd.to_datetime(df_hourly['time'])
            
            current_data_row = df_hourly[df_hourly['time'] == target_timestamp].iloc[0]
            radiation_sum = data['daily']['shortwave_radiation_sum'][0]

            new_row = pd.Series(index=CSV_COLUMNS, dtype='object')
            new_row['timestamp'] = target_timestamp
            for col in HOURLY_VARS:
                new_row[col] = current_data_row[col]
            new_row['shortwave_radiation_sum'] = radiation_sum
            
            new_row['hour_of_day'] = target_timestamp.hour
            new_row['day_of_week'] = target_timestamp.weekday()
            new_row['month_of_year'] = target_timestamp.month
            new_row['is_weekend'] = new_row['day_of_week'] >= 5
            
            df_to_append = pd.DataFrame([new_row])

            filename = f"realtime_data_{station_name}.csv"
            file_exists = os.path.exists(filename)
            
            print(f"Añadiendo datos al archivo: {filename}")
            df_to_append.to_csv(filename, mode='a', header=not file_exists, index=False)
            
            if not file_exists:
                print("El archivo no existía, se ha creado con los encabezados correctos.")
            print(f"✅ Datos para {station_name} guardados exitosamente.")

        except Exception as e:
            print(f"❌ Ocurrió un error al procesar {station_name}: {e}")

# --- 3. BUCLE DE EJECUCIÓN INFINITO ---
if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print(f"Iniciando ciclo de captura: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        ejecutar_captura_una_vez()
        
        # --- Lógica de espera hasta la próxima hora ---
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=2, second=0, microsecond=0)
        
        wait_seconds = (next_hour - now).total_seconds()
        
        print("\n" + "="*50)
        print(f"Captura completada. Próxima ejecución a las: {next_hour.strftime('%H:%M:%S')}")
        print(f"Esperando durante {int(wait_seconds / 60)} minutos...")
        print("="*50)
        
        time.sleep(wait_seconds)