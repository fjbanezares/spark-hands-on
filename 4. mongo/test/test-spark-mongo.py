from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row
import pymongo


# Creamos una sesión de Spark
spark = SparkSession.builder \
    .appName("Ejemplo de conexión a MongoDB Atlas") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:2.4.0") \
    .getOrCreate()

# Leemos los datos de un archivo CSV
df = spark.read.format("csv").option("header", "true").load("archivo.csv")

# Creamos la conexión a MongoDB Atlas
df.write.format("mongo").option("uri", "mongodb+srv://fjbanezares:7ruti5ne@cluster0.mongodb.net/test").mode("overwrite").save()

# Leemos los datos de MongoDB Atlas
df_mongo = spark.read.format("mongo").option("uri", "mongodb+srv://fjbanezares:7ruti5ne@cluster0.mongodb.net/test").load()
df_mongo.show()
