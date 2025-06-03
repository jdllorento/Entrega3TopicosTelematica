import requests
import json
import boto3
import os
from datetime import date

# Parámetros de consulta
params = {
    "latitude": 6.25,
    "longitude": -75.56,
    "start_date": "2024-01-01",
    "end_date": str(date.today()),
    "daily": [
        "temperature_2m_max", "wind_speed_10m_max", "daylight_duration",
        "precipitation_sum", "precipitation_probability_max", "temperature_2m_min",
        "wind_direction_10m_dominant", "sunrise", "sunset",
        "apparent_temperature_max", "apparent_temperature_min", "rain_sum"
    ],
    "timezone": "America/Bogota"
}

url = "https://archive-api.open-meteo.com/v1/archive"
filename = f"weather_medellin{date.today()}.json"
bucket = "open-meteo-bucket-batchproject"
s3_key = f"raw/{filename}"

# Verificar si ya existe el archivo en S3
s3 = boto3.client("s3")
existing = s3.list_objects_v2(Bucket=bucket, Prefix=s3_key)
if any(obj['Key'] == s3_key for obj in existing.get("Contents", [])):
    print(f"⏭️ El archivo de hoy ya existe en S3: {s3_key}")
    exit(0)

# Descargar datos
response = requests.get(url, params=params)
data = response.json()

# Guardar localmente
with open(filename, "w") as f:
    json.dump(data, f)

# Subir a S3
s3.upload_file(filename, bucket, s3_key)
print(f"✅ Archivo subido a S3: s3://{bucket}/{s3_key}")

# Eliminar archivo local
try:
    os.remove(filename)
    print(f"🧹 Archivo local eliminado: {filename}")
except Exception as e:
    print(f"⚠️ No se pudo eliminar el archivo local: {e}")
