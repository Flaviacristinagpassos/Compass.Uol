import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


# Definindo o esquema para o DataFrame
schema_movies = StructType([
    StructField("id", IntegerType(), True),
    StructField("tituloPrincipal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notamedia", FloatType(), True)
])

schema_series = StructType([
    StructField("id", IntegerType(), True),
    StructField("tituloPrincipal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notamedia", FloatType(), True)
])

# Definir os caminhos da Raw Zone (origem) e Trusted Zone (destino)
raw_zone_path_movies = "s3://data-lake-flavia-passos/Raw/Local/CSV/Movies/"
raw_zone_path_series = "s3://data-lake-flavia-passos/Raw/Local/CSV/Series/"
trusted_zone_path_movies = "s3://data-lake-flavia-passos/trusted/movies/"
trusted_zone_path_series = "s3://data-lake-flavia-passos/trusted/series/"

# Definindo os caminhos da Raw Zone (origem) e Trusted Zone (destino)
df_raw_movies = spark.read.format("csv").option("header", "true").schema(schema_movies).load(raw_zone_path_movies)
df_raw_series = spark.read.format("csv").option("header", "true").schema(schema_series).load(raw_zone_path_series)

# Realizar as transformações necessárias (limpeza, padronização)
df_clean_movies = df_raw_movies.dropna(how="all") 
df_clean_series = df_raw_series.dropna(how="all")

# Gravar os dados transformados na Trusted Zone em formato Parquet
df_clean_movies.write.mode("overwrite").format("parquet").save(trusted_zone_path_movies)
df_clean_series.write.mode("overwrite").format("parquet").save(trusted_zone_path_series)

# Finalizar o job
job.commit()
