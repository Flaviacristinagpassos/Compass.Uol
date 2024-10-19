from pyspark.sql import SparkSession
from pyspark import SparkContext, SQLContext
from pyspark.sql.functions import col, when, rand, expr, udf
from random import choice

# Etapa 1: Criar SparkSession e carregar o arquivo
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .getOrCreate()

df_nomes = spark.read.csv("nomes_aleatorios.txt", header=False, inferSchema=True)
df_nomes.show(5)

# Etapa 2: Renomear coluna e imprimir esquema
df_nomes = df_nomes.withColumnRenamed("_c0", "Nome")
df_nomes.printSchema()
df_nomes.show(10)

# Etapa 3: Adicionar coluna "Escolaridade"
df_nomes = df_nomes.withColumn(
    "Escolaridade", 
    when(rand() < 0.33, "Fundamental")
    .when((rand() >= 0.33) & (rand() < 0.66), "Medio")
    .otherwise("Superior")
)

df_nomes.show(10)

# Etapa 4: Adicionar coluna "País" com países da América do Sul
paises = ["Argentina", "Brasil", "Chile", "Colômbia", "Equador", "Guiana", "Paraguai", "Peru", "Suriname", "Uruguai", "Venezuela", "Bolívia", "Guiana Francesa"]


# Função para selecionar país aleatório
@udf
def pais_aleatorio():
    return choice(paises)

# Adicionar a clonuna
df_nomes = df_nomes.withColumn("Pais", pais_aleatorio())
df_nomes.show(10)

# Etapa 5: Adicionar coluna "AnoNascimento" com valores aleatórios
df_nomes = df_nomes.withColumn("AnoNascimento", (rand() * (2010 - 1945) + 1945).cast("int"))
df_nomes.show(10)

# Etapa 6: Selecionar pessoas nascidas no século 21
df_select = df_nomes.filter(df_nomes.AnoNascimento >= 2000)
df_select.show(10)

# Etapa 7: Usar Spark SQL para selecionar pessoas nascidas no século 21
# Registrar o DataFrame como tabela temporária
df_nomes.createOrReplaceTempView("pessoas")

# SQL para selecionar pessoas nascidas a partir de 2000
spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000").show(10)

# Etapa 8: Contar Millenials
millennials_count = df_nomes.filter((df_nomes.AnoNascimento >= 1980) & (df_nomes.AnoNascimento <= 1994)).count()
print(f"Número de Millenials: {millennials_count}")

# Etapa 9: Contar Millenials usando Spark SQL
spark.sql("SELECT COUNT(*) FROM pessoas WHERE AnoNascimento BETWEEN 1980 AND 1994").show()

# Etapa 10: Contar pessoas de cada geração por país
geracoes_sql = """
SELECT Pais, 
       CASE
           WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
           WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geracao X'
           WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
           WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geracao Z'
       END AS Geracao, 
       COUNT(*) AS Quantidade
FROM pessoas
GROUP BY Pais, Geracao
ORDER BY Pais, Geracao
"""

# Executar a consulta e mostrar resultado
df_geracoes = spark.sql(geracoes_sql)
df_geracoes.show()

