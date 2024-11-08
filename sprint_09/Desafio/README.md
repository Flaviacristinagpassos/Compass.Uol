## O objetivo é integrar dados de fontes variadas, processá-los em diferentes camadas e permitir análises analíticas baseadas nesses dados. Nesta etapa será a entrega da parte 4

# Estrutura do Pipeline
1. Ingestão de Dados
    - Fonte dos Dados: Utilizamos arquivos CSV para dados brutos de filmes e séries, além de dados complementares da API do TMDB.
    - Ferramentas Utilizadas: AWS Lambda para ingestão de dados da API e AWS Glue para processamento.
    - Processo: Os dados CSV foram carregados para a Raw Zone e dados da API foram salvos em JSON no Amazon S3, com até 100 registros por arquivo.

2. Transformação e Processamento
    - Objetivo: Organizar os dados na camada Trusted Zone e, posteriormente, na Refined Zone para análise.
    - Processo de Enriquecimento: A partir dos dados brutos e dados externos da API, os dados foram organizados e filtrados para atender aos requisitos de categorias específicas (Drama e Romance).
    - Tecnologia: Usamos Spark no AWS Glue para manipulação e transformação de dados.

3. Criação de Tabelas na Refined Zone

- O código abaixo realiza o processamento dos dados da Trusted Zone para criar a Tabela de Fatos e as Dimensões.

```Python
# Importa a biblioteca necessária para funções de agregação e manipulação de dados
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# Inicializa uma sessão Spark com o nome "Refined_Processamento_Drama_Romance"
spark = SparkSession.builder.appName("Refined_Processamento_Drama_Romance").getOrCreate()

# Leitura dos dados da Trusted Zone
# Aqui, estamos carregando o arquivo Parquet da camada Trusted para um DataFrame chamado trusted_df
trusted_df = spark.read.parquet("s3://data-lake-flavia-passos/Trusted/API/Movies/arquivo.snappy.parquet")

# Verificar o esquema e as primeiras linhas
# Essas linhas são usadas para inspecionar os dados e garantir que o esquema e os dados lidos estejam corretos
trusted_df.printSchema()
trusted_df.show(5)

# Criando a Tabela de Fatos - FatoFilmes
# Filtramos os dados para os gêneros "Drama" e "Romance" e realizamos uma agregação
# Aqui estamos agrupando os dados por "id" (ID do filme) e "genre_name" (nome do gênero)
fato_filmes_df = trusted_df.filter(trusted_df["genre_name"].isin("Drama", "Romance")) \
    .groupBy("id", "genre_name") \
    .agg(
        F.countDistinct("title").alias("qtd_titulos"),  # Conta o número distinto de títulos por gênero e ID
        F.count("id").alias("total_filmes")  # Conta o total de ocorrências do ID (filmes) para cada gênero
    )

# Salvar a Tabela de Fatos na camada Refined
# Escrevemos o DataFrame da tabela de fatos no Amazon S3 em formato Parquet, na camada Refined
fato_filmes_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/FatoFilmes/")

# Criando a Dimensão DimFilme
# Selecionamos apenas as colunas "id" e "title" (título), garantindo que cada filme seja único com `distinct`
dim_filme_df = trusted_df.select("id", "title").distinct()

# Salvando a DimFilme na camada Refined
dim_filme_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/DimFilme/")

# Criando a Dimensão DimGenero
# Selecionamos as colunas "genre_name" e "id" para criar a dimensão de gênero, removendo duplicatas
dim_genero_df = trusted_df.select("genre_name").distinct()

# Salvando a DimGenero na camada Refined
dim_genero_df.write.mode("overwrite").parquet("s3://data-lake-flavia-passos/Refined/DimGenero/")

# Finaliza o trabalho Spark
job.commit()
```

# Conclusão
O desafio de construção do Data Lake para a categoria Drama e Romance foi bem-sucedido. Utilizando AWS Glue, Lambda, e Spark, foi implementado um pipeline robusto que organiza os dados em camadas, do bruto ao refinado, garantindo uma estrutura escalável e eficiente para análises futuras. A divisão dos dados em tabelas de fatos e dimensões na Refined Zone permite uma análise estruturada e categorizada, facilitando o acesso aos dados específicos de filmes e séries de Drama e Romance. Este projeto fornece uma base sólida para exploração e insights, com potencial para expansão para outras categorias e integrações.