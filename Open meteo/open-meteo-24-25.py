import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN DEL CLIENTE DE LA API ---
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)
url = "https://archive-api.open-meteo.com/v1/archive"

# --- 2. FUNCIÓN PARA OBTENER DATOS (sin cambios) ---
def obtener_datos_meteorologicos(latitud, longitud, fecha_inicio, fecha_fin, timezone):
    params = {
        "latitude": latitud, "longitude": longitud, "start_date": fecha_inicio, "end_date": fecha_fin,
        "daily": "shortwave_radiation_sum",
        "hourly": ["temperature_2m", "relativehumidity_2m", "precipitation", "pressure_msl", 
                   "windspeed_10m", "winddirection_10m", "boundary_layer_height"],
        "timezone": timezone 
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    hourly = response.Hourly()
    timezone_str = response.Timezone().decode("utf-8")

    utc_dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    hourly_data = {"date": utc_dates.tz_convert(timezone_str)}
    
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["relativehumidity_2m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["precipitation"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["pressure_msl"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["windspeed_10m"] = hourly.Variables(4).ValuesAsNumpy()
    hourly_data["winddirection_10m"] = hourly.Variables(5).ValuesAsNumpy()
    hourly_data["boundary_layer_height"] = hourly.Variables(6).ValuesAsNumpy()
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    
    daily = response.Daily()
    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["shortwave_radiation_sum"] = daily.Variables(0).ValuesAsNumpy()
    daily_dataframe = pd.DataFrame(data=daily_data)
    
    return hourly_dataframe, daily_dataframe

# --- 3. FUNCIÓN DE PROCESAMIENTO (MODIFICADA) ---
def procesar_datos(hourly_df, daily_df, station_id):
    hourly_df['date_only'] = hourly_df['date'].dt.date
    daily_df['date_only'] = daily_df['date'].dt.date
    
    merged_df = pd.merge(hourly_df, daily_df[['date_only', 'shortwave_radiation_sum']], on='date_only', how='left')
    merged_df.rename(columns={'date': 'timestamp'}, inplace=True)
    
    # CAMBIOS AQUÍ: Se añaden las nuevas columnas y se corrige el formato de las anteriores
    merged_df['hour_of_day'] = merged_df['timestamp'].dt.hour
    merged_df['day_of_week'] = merged_df['timestamp'].dt.weekday  # Formato 0-6
    merged_df['month_of_year'] = merged_df['timestamp'].dt.month
    merged_df['is_weekend'] = merged_df['day_of_week'] >= 5     # Sábado(5) o Domingo(6)

    # Se actualiza la lista de columnas final
    columnas_finales = [
        'timestamp', 'temperature_2m', 'relativehumidity_2m', 'precipitation',
        'pressure_msl', 'windspeed_10m', 'winddirection_10m',
        'boundary_layer_height', 'shortwave_radiation_sum',
        'hour_of_day', 'day_of_week', 'month_of_year', 'is_weekend'
    ]
    
    return merged_df[columnas_finales]

# --- 4. FUNCIÓN EJECUTORA (sin cambios) ---
def ejecutar_proceso_completo(estaciones, fecha_inicio_total, fecha_fin_total, prefijo_archivo_csv):
    rangos_de_fechas = pd.date_range(start=fecha_inicio_total, end=fecha_fin_total, freq='3MS')

    for station_name, info in estaciones.items():
        print(f"\n--- Procesando estación completa: {station_name} ---")
        lista_df_estacion_actual = []

        for i in range(len(rangos_de_fechas)):
            start_chunk = rangos_de_fechas[i]
            if i + 1 < len(rangos_de_fechas):
                end_chunk = rangos_de_fechas[i+1] - pd.Timedelta(days=1)
            else:
                end_chunk = datetime.strptime(fecha_fin_total, '%Y-%m-%d')

            print(f"Obteniendo datos para {station_name} desde {start_chunk.strftime('%Y-%m-%d')} hasta {end_chunk.strftime('%Y-%m-%d')}")
            
            hourly_df, daily_df = obtener_datos_meteorologicos(
                latitud=info["lat"], longitud=info["lon"],
                fecha_inicio=start_chunk.strftime('%Y-%m-%d'), fecha_fin=end_chunk.strftime('%Y-%m-%d'),
                timezone=info["tz"]
            )
            
            df_procesado = procesar_datos(hourly_df, daily_df, station_name)
            lista_df_estacion_actual.append(df_procesado)
        
        print(f"Combinando datos para {station_name}...")
        df_final_estacion = pd.concat(lista_df_estacion_actual, ignore_index=True)
        nombre_archivo_final = f"{prefijo_archivo_csv}_{station_name}_24h.csv"
        
        print(f"Guardando archivo para {station_name} en: {nombre_archivo_final}")
        df_final_estacion.to_csv(nombre_archivo_final, index=False)
        print(f"✅ Archivo para {station_name} guardado.")

    print("\n🎉 ¡Proceso completado para todas las estaciones!")

# --- 5. CONFIGURACIÓN Y EJECUCIÓN DEL SCRIPT ---
if __name__ == '__main__':
    ESTACIONES = {
        "Centro_CDMX": {"lat": 19.43, "lon": -99.13, "tz": "auto"},
        "Centro_LA": {"lat": 34.05, "lon": -118.24, "tz": "America/Los_Angeles"}
    }
    FECHA_INICIO = "2024-01-01"
    FECHA_FIN = "2025-10-04"
    PREFIJO_ARCHIVO_CSV = "datos_finales_ml"
    
    ejecutar_proceso_completo(ESTACIONES, FECHA_INICIO, FECHA_FIN, PREFIJO_ARCHIVO_CSV)