import pandas as pd

# Define el nombre de tu archivo de entrada y el de salida
archivo_entrada = 'dataset_final_LA_limpio.csv'
archivo_salida = 'dataset_LA_con_prediccion.csv'

try:
    # 1. Cargar el dataset
    # Es importante parsear la columna 'timestamp' como una fecha
    print(f"Cargando el archivo: {archivo_entrada}...")
    df = pd.read_csv(archivo_entrada, parse_dates=['timestamp'])

    # 2. Ordenar por fecha (es crucial para que el 'shift' funcione correctamente)
    df.sort_values(by='timestamp', inplace=True)

    # 3. Crear la columna 'pm25_prediction'
    # Usamos shift(-24) para tomar el valor de 24 filas más adelante (el día siguiente a la misma hora)
    print("Generando la columna 'pm25_prediction'...")
    df['pm25_prediction'] = df['pm25'].shift(-24)

    # 4. Mostrar las primeras filas para verificar el resultado
    print("\n--- Vista previa de los datos con la nueva columna ---")
    print(df[['timestamp', 'pm25', 'pm25_prediction']].head())
    
    # 5. Mostrar las últimas filas para verificar los valores NaN
    print("\n--- Vista previa de las últimas filas (con valores Nulos) ---")
    print(df[['timestamp', 'pm25', 'pm25_prediction']].tail())

    # 6. Guardar el nuevo dataset en un archivo CSV
    print(f"\nGuardando los resultados en: {archivo_salida}...")
    df.to_csv(archivo_salida, index=False)

    print(f"\n✅ ¡Proceso completado exitosamente! El archivo '{archivo_salida}' ha sido creado.")

except FileNotFoundError:
    print(f"\n❌ ERROR: El archivo '{archivo_entrada}' no se pudo encontrar.")
    print("Asegúrate de que este script esté en la misma carpeta que tu archivo CSV.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")