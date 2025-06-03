from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min

spark = SparkSession.builder.appName("DescriptiveStats").getOrCreate()

# Cargar datos de zona trusted (por ejemplo en formato .csv)
df = spark.read.option("header", True).csv("s3://open-meteo-bucket-batchproject/trusted/**/*.csv")

df.show()

# Filtrar columnas relevantes

# Convertir a tipos adecuados
df = df.withColumn("temp_max", col("temp_max").cast("float"))

# Análisis descriptivo
summary = df.select(
    avg("temp_max").alias("avg_temp"),
    max("temp_max").alias("max_temp"),
    min("temp_max").alias("min_temp")
)

# Guardar resultados en zona refined
summary.coalesce(1).write.mode("overwrite").csv("s3://open-meteo-bucket-batchproject/refined/descriptive_stats/", header=True)