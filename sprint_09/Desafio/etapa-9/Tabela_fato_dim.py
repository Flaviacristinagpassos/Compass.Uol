```Python
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Refined_Processamento_Drama_Romance").getOrCreate()

trusted_df = spark.read.parquet("s3://data-lake-flavia-passos/Trusted/API/Movies/arquivo.snappy.parquet")
trusted_df.printSchema()
trusted_df.show(5)

fato_filmes_df = trusted_df.filter(trusted_df["genre_name"].isin("Drama", "Romance")) \
    .groupBy("id", "genre_name") \
    .agg(
        F.countDistinct("title").alias("qtd_titulos"), 
        F.count("id").alias("total_filmes") 

fato_filmes_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/FatoFilmes/")
dim_filme_df = trusted_df.select("id", "title").distinct()
dim_filme_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/DimFilme/")

dim_genero_df = trusted_df.select("genre_name").distinct()
dim_genero_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/DimGenero/")

job.commit()
```