from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min

spark = SparkSession.builder.appName("DescriptiveStats").getOrCreate()

# Cargar datos de zona trusted (por ejemplo en formato .csv)
df = spark.read.option("header", True).csv("s3a://open-meteo-bucket-batchproject/trusted/**/*.csv")

df.show()

# Filtrar columnas relevantes

# Convertir a tipos adecuados
df = df.withColumn("temperature_2m_max", col("temperature_2m_max").cast("float"))

# Análisis descriptivo
summary = df.select(
    avg("temperature_2m_max").alias("avg_temp"),
    max("temperature_2m_max").alias("max_temp"),
    min("temperature_2m_max").alias("min_temp")
)

# Guardar resultados en zona refined
summary.coalesce(1).write.mode("overwrite").csv("s3a://open-meteo-bucket-batchproject/refined/descriptive_stats/", header=True)