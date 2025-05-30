from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, to_date
import boto3
import re
import os
import json

# Crear sesión de Spark
spark = SparkSession.builder.appName("DataPrepOpenMeteo").getOrCreate()

# Parámetros
bucket = "open-meteo-bucket-batchproject"
raw_prefix = "raw/"
trusted_prefix = "trusted/"
pattern = r"weather_medellin(\d{4}-\d{2}-\d{2})\.json"

# Listar archivos en S3
s3 = boto3.client("s3")
response = s3.list_objects_v2(Bucket=bucket, Prefix=raw_prefix)
files = [
    obj["Key"] for obj in response.get("Contents", [])
    if re.match(f"{raw_prefix}weather_medellin\\d{{4}}-\\d{{2}}-\\d{{2}}\\.json", obj["Key"])
]

if not files:
    raise Exception("❌ No se encontraron archivos JSON en la carpeta raw/")

# Tomar archivo más reciente
latest_file = sorted(files)[-1]
print(f"📂 Archivo encontrado: {latest_file}")

# Extraer fecha del nombre
match = re.search(pattern, latest_file)
fecha = match.group(1) if match else "unknown"
print(f"📅 Fecha extraída: {fecha}")

# Descargar a local
local_path = f"/tmp/weather_{fecha}.json"
s3.download_file(bucket, latest_file, local_path)

# Cargar y parsear JSON
with open(local_path, "r") as f:
    data = json.load(f)

daily = data["daily"]
variables = [key for key in daily if key != "time"]
valid_variables = [
    var for var in variables if any(daily[var][i] is not None for i in range(len(daily["time"])))
]

print(f"✅ Variables válidas detectadas: {valid_variables}")

# Crear filas
rows = []
for i in range(len(daily["time"])):
    row = {"date": daily["time"][i]}
    for var in valid_variables:
        row[var] = daily[var][i]
    rows.append(Row(**row))

# Crear DataFrame
df = spark.createDataFrame(rows)

# Limpieza
df_clean = (
    df.dropna()
      .dropDuplicates()
      .withColumn("date", to_date(col("date")))
)

# Escribir a zona trusted
output_path = f"s3a://{bucket}/{trusted_prefix}weather_{fecha}.csv"
print(f"📝 Guardando resultado en: {output_path}")
df_clean.write.mode("overwrite").csv(output_path, header=True)

# Eliminar archivo local temporal
os.remove(local_path)
print("🧹 Archivo temporal eliminado.")
