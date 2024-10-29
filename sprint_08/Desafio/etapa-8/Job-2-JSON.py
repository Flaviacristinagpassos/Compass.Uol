import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, MapType
from pyspark.sql.functions import explode, col 

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Definir os caminhos da Raw Zone (origem) e Trusted Zone (destino)
raw_zone_path_tmdb = "s3://data-lake-flavia-passos/Raw/API/Movies"
trusted_zone_path_tmdb = "s3://data-lake-flavia-passos/Trusted/API/Movies/"

# Definir o esquema manualmente com base nos campos dos arquivos JSON
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("release_date", StringType(), True),
    StructField("genres", ArrayType(MapType(StringType(), StringType())), True),
])

# Usar o esquema definido ao carregar os dados JSON
df_raw_json = spark.read.format("json").schema(schema).load(raw_zone_path_tmdb)

# Transformação: Extrair apenas os nomes dos gêneros
df_exploded = df_raw_json.withColumn("genre_name_exploded", explode(col("genres"))).select(
    "*",
    col("genre_name_exploded.name").alias("genre_name")
)

# Remover a coluna temporária "genre_name_exploded" se ainda existir
df_clean_json = df_exploded.drop("genre_name_exploded").withColumnRenamed("original_title", "titulo")

# Salvar o DataFrame transformado na Trusted Zone em formato Parquet
df_clean_json.write.mode("overwrite").format("parquet").save(trusted_zone_path_tmdb)

job.commit()
