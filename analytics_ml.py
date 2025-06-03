from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# Crear sesión de Spark
spark = SparkSession.builder.appName("AdvancedAnalytics").getOrCreate()

# Leer datos de zona trusted
df = spark.read.option("header", True).csv("s3://open-meteo-bucket-batchproject/trusted/**/*.csv")

# Preprocesamiento
features = ["temp_max", "precip"]
df = df.select(*(col(f).cast("float") for f in features)).na.drop()

assembler = VectorAssembler(inputCols=features, outputCol="features")
df_vec = assembler.transform(df)

# Modelo de clustering
kmeans = KMeans(k=3, seed=42)
model = kmeans.fit(df_vec)

# Predicciones
predictions = model.transform(df_vec)

# Guardar resultados en refined
predictions.select("features", "prediction").coalesce(1).write.mode("overwrite").csv("s3://open-meteo-bucket-batchproject/refined/clustering_results/", header=True)