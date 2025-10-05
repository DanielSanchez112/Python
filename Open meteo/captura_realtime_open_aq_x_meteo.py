import pandas as pd
from datetime import datetime, timedelta, timezone
import os
import time
import urllib.request
import urllib.parse
import json
from dotenv import load_dotenv

# --- 1. CONFIGURACIÓN ---
load_dotenv()
API_KEY_OPENAQ = os.getenv("API_KEY_OPENAQ")
if not API_KEY_OPENAQ:
    raise ValueError("No se encontró la API Key. Asegúrate de crear un archivo .env con API_KEY_OPENAQ.")

STATIONS = {
    "Centro_CDMX": {"lat": 19.43, "lon": -99.13, "tz_api": "auto"},
    "Centro_LA": {"lat": 34.05, "lon": -118.24, "tz_api": "America/Los_Angeles"}
}

CSV_COLUMNS = [
    'timestamp', 'temperature_2m', 'relativehumidity_2m', 'precipitation', 'pressure_msl',
    'windspeed_10m', 'winddirection_10m', 'boundary_layer_height', 'shortwave_radiation_sum',
    'hour_of_day', 'day_of_week', 'month_of_year', 'is_weekend',
    'co', 'no', 'no2', 'nox', 'o3', 'pm25', 'so2'
]

# Mapeo de parámetros de OpenAQ a nuestros nombres de columna
PARAMETER_MAPPING = {
    'co ppm': 'co',
    'no ppm': 'no',
    'no2 ppm': 'no2', 
    'nox ppm': 'nox',
    'o3 ppm': 'o3',
    'pm25 µg/m³': 'pm25',
    'so2 ppm': 'so2'
}

# --- 2. FUNCIONES PARA LLAMAR A LAS APIS ---

def get_openaq_data(lat, lon, api_key):
    """Obtiene los últimos datos de calidad del aire de OpenAQ."""
    print("...Iniciando petición a OpenAQ...")
    air_quality_data = {}
    
    try:
        # Paso 1: Obtener ubicaciones cercanas
        base_url = "https://api.openaq.org/v3/locations"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": 10000,  # 10km radius
            "limit": 5
        }
        headers = {"X-API-Key": api_key}
        
        locations_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"...Buscando ubicaciones: {locations_url}")
        
        req = urllib.request.Request(locations_url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                locations_data = json.loads(response.read().decode("utf-8"))
                
                if locations_data.get('results'):
                    print(f"...Encontradas {len(locations_data['results'])} ubicaciones")
                    
                    # Buscar la ubicación con más parámetros disponibles
                    best_location = None
                    max_params = 0
                    
                    for location in locations_data['results']:
                        sensors = location.get('sensors', [])
                        sensor_params = [s['name'] for s in sensors]
                        target_params_count = sum(1 for param in sensor_params if param in PARAMETER_MAPPING)
                        
                        print(f"...Ubicación: {location['name']} - Parámetros objetivo: {target_params_count}")
                        
                        if target_params_count > max_params:
                            max_params = target_params_count
                            best_location = location
                    
                    if best_location:
                        location_id = best_location['id']
                        print(f"...Usando ubicación: {best_location['name']} (ID: {location_id})")
                        
                        # Crear mapeo de sensor ID a parámetro para esta ubicación
                        sensor_mapping = {}
                        for sensor in best_location.get('sensors', []):
                            sensor_id = sensor['id']
                            sensor_name = sensor['name']
                            sensor_mapping[sensor_id] = sensor_name
                        
                        print(f"...Mapeo de sensores creado para {len(sensor_mapping)} sensores")
                        
                        # Paso 2: Obtener mediciones más recientes
                        measurements_url = f"https://api.openaq.org/v3/locations/{location_id}/latest"
                        print(f"...Obteniendo mediciones: {measurements_url}")
                        
                        req = urllib.request.Request(measurements_url, headers=headers)
                        
                        with urllib.request.urlopen(req) as response:
                            if response.status == 200:
                                measurements_data = json.loads(response.read().decode("utf-8"))
                                
                                if measurements_data.get('results'):
                                    print(f"...Procesando {len(measurements_data['results'])} mediciones")
                                    
                                    # Procesar las mediciones usando el mapeo de sensores
                                    for measurement in measurements_data['results']:
                                        sensor_id = measurement.get('sensorsId')
                                        value = measurement.get('value')
                                        
                                        if sensor_id in sensor_mapping:
                                            param_name = sensor_mapping[sensor_id]
                                            
                                            if param_name in PARAMETER_MAPPING:
                                                mapped_param = PARAMETER_MAPPING[param_name]
                                                air_quality_data[mapped_param] = value
                                                print(f"...✓ {mapped_param}: {value}")
                                
                                print(f"...Datos de calidad del aire obtenidos: {len(air_quality_data)} parámetros")
                            else:
                                print(f"...Error obteniendo mediciones: código {response.status}")
                    else:
                        print("...No se encontró una ubicación adecuada con parámetros objetivo")
                else:
                    print("...No se encontraron ubicaciones cercanas")
            else:
                print(f"...Error obteniendo ubicaciones: código {response.status}")

    except urllib.error.HTTPError as e:
        print(f"--- ERROR HTTP en OpenAQ ---")
        print(f"Código de estado: {e.code}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Respuesta del servidor: {error_body}")
        except:
            print("No se pudo leer la respuesta del error")
    except Exception as e:
        print(f"--- ERROR inesperado en OpenAQ: {e} ---")

    return air_quality_data

def get_openmeteo_data(lat, lon, timezone, start_date, end_date):
    """Obtiene datos climáticos de Open-Meteo."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon, "timezone": timezone,
        "start_date": start_date, "end_date": end_date,
        "hourly": ["temperature_2m", "relativehumidity_2m", "precipitation", "pressure_msl", 
                   "windspeed_10m", "winddirection_10m", "boundary_layer_height"],
        "daily": ["shortwave_radiation_sum"]
    }
    hourly_params = "&".join([f"hourly={var}" for var in params['hourly']])
    daily_params = "&".join([f"daily={var}" for var in params['daily']])
    del params['hourly'], params['daily']
    
    full_url = f"{base_url}?{urllib.parse.urlencode(params)}&{hourly_params}&{daily_params}"
    
    with urllib.request.urlopen(full_url) as response:
        if response.status != 200:
            raise Exception(f"API Open-Meteo falló con código {response.status}")
        return json.loads(response.read().decode("utf-8"))

# --- 3. FUNCIÓN PRINCIPAL DE CAPTURA ---
def ejecutar_captura_una_vez():
    now_utc = datetime.now(timezone.utc)  # Corregido para evitar deprecation warning
    now_cdmx = now_utc - timedelta(hours=6)
    now_la = now_cdmx - timedelta(hours=1)
    station_times = {"Centro_CDMX": now_cdmx, "Centro_LA": now_la}

    for station_name, info in STATIONS.items():
        print(f"\n--- Procesando estación: {station_name} ---")
        try:
            current_time = station_times[station_name]
            target_timestamp = current_time.replace(minute=0, second=0, microsecond=0)
            
            print(f"Hora local calculada: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Obteniendo datos para la hora: {target_timestamp.strftime('%Y-%m-%d %H:00:00')}")

            # Obtener datos de ambas APIs
            weather_data = get_openmeteo_data(info["lat"], info["lon"], info["tz_api"], target_timestamp.strftime('%Y-%m-%d'), target_timestamp.strftime('%Y-%m-%d'))
            air_quality_data = get_openaq_data(info["lat"], info["lon"], API_KEY_OPENAQ)

            # Procesar y combinar los datos
            df_hourly = pd.DataFrame(weather_data['hourly'])
            df_hourly['time'] = pd.to_datetime(df_hourly['time'])
            
            # Convertir target_timestamp a naive datetime para que coincida con los datos de Open-Meteo
            target_timestamp_naive = target_timestamp.replace(tzinfo=None)
            current_weather_row = df_hourly[df_hourly['time'] == target_timestamp_naive].iloc[0]
            radiation_sum = weather_data['daily']['shortwave_radiation_sum'][0]

            new_row = pd.Series(index=CSV_COLUMNS, dtype='object')
            new_row['timestamp'] = target_timestamp
            
            # Añadir datos meteorológicos
            for col in current_weather_row.index:
                if col in new_row.index:
                    new_row[col] = current_weather_row[col]
            new_row['shortwave_radiation_sum'] = radiation_sum
            
            # Añadir datos de calidad del aire
            for param, value in air_quality_data.items():
                if param in new_row.index:
                    new_row[param] = value
            
            # Añadir características temporales
            new_row['hour_of_day'] = target_timestamp.hour
            new_row['day_of_week'] = target_timestamp.weekday()
            new_row['month_of_year'] = target_timestamp.month
            new_row['is_weekend'] = new_row['day_of_week'] >= 5
            
            df_to_append = pd.DataFrame([new_row])

            # Añadir al archivo CSV
            filename = f"realtime_data_{station_name}.csv"
            file_exists = os.path.exists(filename)
            df_to_append.to_csv(filename, mode='a', header=not file_exists, index=False)
            
            print(f"✅ Datos combinados guardados en {filename}")
            print(f"   Meteorología: ✓")
            print(f"   Calidad del aire: {len(air_quality_data)} parámetros")

        except Exception as e:
            print(f"❌ Error procesando {station_name}: {e}")

# --- 4. FUNCIÓN DE EJECUCIÓN CONTINUA ---
def ejecutar_continuamente():
    """Ejecuta la captura cada hora automáticamente."""
    while True:
        print("\n" + "="*60)
        print(f"Iniciando ciclo de captura: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        ejecutar_captura_una_vez()
        
        # Calcular el tiempo hasta la próxima hora
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=2, second=0, microsecond=0)
        wait_seconds = (next_hour - now).total_seconds()
        
        print("\n" + "="*60)
        print(f"Captura completada. Próxima ejecución: {next_hour.strftime('%H:%M:%S')}")
        print(f"Esperando {int(wait_seconds / 60)} minutos...")
        print("="*60)
        
        time.sleep(wait_seconds)

# --- 5. SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--prueba":
        print("🧪 Ejecutando captura de prueba única")
        print("Para ejecutar continuamente, ejecuta sin parámetros")
        print("\n" + "="*50)
        print(f"Captura de prueba: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        ejecutar_captura_una_vez()
        
        print("\n" + "="*50)
        print("✅ Captura de prueba completada exitosamente!")
        print("Los datos se guardaron en los archivos CSV.")
        print("="*50)
    else:
        print("🔄 Iniciando modo continuo (cada hora)")
        print("Para ejecutar solo una vez, usa: python captura_realtime_open_aq_x_meteo.py --prueba")
        print("Presiona Ctrl+C para detener")
        try:
            ejecutar_continuamente()
        except KeyboardInterrupt:
            print("\n🛑 Captura detenida por el usuario")