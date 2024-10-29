# Este projeto contém o código e as evidências desenvolvidas para a entrega 3 do desafio de construção de um Data Lake<img align="center" width=80 height=70 src="https://files.cdata.com/media/media/izvfwdfj/what-is-a-data-lake.png" />

O objetivo principal desta etapa é realizar a ingestão e o processamento de dados utilizando o AWS Glue e o Apache Spark, movendo dados da Raw Zone para a Trusted Zone do Data Lake. O desafio envolve a integração de dados de filmes e séries, oriundos de arquivos CSV e da API do TMDB, é a entrega 3 de um desafio para a construção de um Data Lake utilizando serviços da AWS.

## Estrutura do Projeto

1. Raw Zone: Armazena os dados brutos, provenientes de diferentes fontes.
    - Dados de arquivos CSV (Movies e Series)
    - Dados da API do TMDB (em formato JSON)

2. Trusted Zone: Armazena os dados processados e limpos, que estão prontos para serem consultados no AWS Athena.

# O Desafio envolve a construção de uma pipeline de dados
## Objetivos:
1. Ingerir e processar os arquivos CSV de filmes e séries da Raw Zone para a Trusted Zone.
2. Ingerir e processar os arquivos JSON provenientes da API TMDB.
3. Responder perguntas analíticas relacionadas aos gêneros Drama e Romance, com base nos dados de filmes e séries processados.

## Perguntas Respondidas:
1. **Quantos filmes e séries de Drama e Romance existem?**
    - Resposta: Total de títulos classificados como Drama ou Romance nos arquivos CSV e JSON

2. **Quantos títulos únicos de filmes pertencem aos gêneros Drama e Romance?**
    - Resposta: Contagem de títulos únicos de filmes classificados como Drama ou Romance

3. **Quantos títulos únicos de séries pertencem aos gêneros Drama e Romance?**
    - Resposta: Contagem de títulos únicos de séries classificados como Drama ou Romance

# Jobs Criados no AWS Glue
## Job 1: Processamento dos Arquivos CSV
Este job processa os arquivos CSV de filmes e séries localizados na Raw Zone e os transforma para a Trusted Zone. O código executa as seguintes etapas:
    - Leitura dos arquivos CSV da Raw Zone.
    - Limpeza e padronização dos dados (remoção de linhas vazias).
    - Gravação dos dados processados em formato Parquet na Trusted Zone.

## Job 2: Processamento dos Arquivos JSON
Este job será responsável por processar os dados provenientes da API TMDB, movendo-os para a Trusted Zone.

## Job 3: Análise de Dados
Este job será desenvolvido para realizar as análises necessárias e responder às perguntas analíticas relacionadas aos gêneros Drama e Romance.

## Código

```Python
import os # Interagir com o Sistema Operacional
import json # Manipular dados JSON
import boto3 # Interagir com AWS
import requests # Fazer solicitações HTTP, como chamadas APi
from dotenv import load_dotenv # Carregar variáveis .env
from datetime import datetime # Manipular e formatar Data e Hora
```

A linha 
```Python
from tmdbv3api import TMDb, Movie
```
Foi removida. A importação de TMDb e Movie do pacote tmdbv3api foi removida porque o código não estava utilizando essas classes diretamente para realizar as chamadas de API. Em vez disso, o código usa o módulo requests para fazer requisições HTTP à API do TMDB.
A função get_movies() constrói manualmente a URL da API e faz uma requisição GET usando o requests.get(), assim dispensando o uso do pacote tmdbv3api.

```Python
load_dotenv() # Carregar o arquivo .env

# Acessar as chaves da API
tmdb_api_key = os.getenv('TMDB_API_KEY')
S3_BUCKET = 'data-lake-flavia-passos'
BASE_URL = 'https://api.themoviedb.org/3'

# Configurar cliente do S3
session = boto3.Session(profile_name='AdministratorAccess-529088293312')
s3 = session.client('s3')

def get_movies(page):
    url = f"{BASE_URL}/movie/upcoming?api_key={tmdb_api_key}&language=pt-BR&page={page}" # Monta a URL para a API de filmes futuros, incluindo parâmetros de API Key, idioma e página
    response = requests.get(url) # Faz a solicitação para a API com a URL montada
    
    print(f"URL: {url}")  # Printa a URL chamada no log 
    print(f"Status Code: {response.status_code}")  # Printa o código de status da resposta HTTP para fins de log 
    print(f"Response Text: {response.text}") # Printa o conteúdo da resposta da API para verificação
    
    if response.status_code == 200: # Se a resposta for bem sucedida
    	movies_data = response.json() # Converte a resposta JSON pra um dicionário Python
        print(movies_data)  # Printa os dados dos filmes no console para verificar
        return movies_data  # Retorna os dados dos filmes
    else:
        print(f"Erro ao buscar filmes: {response.status_code} - {response.text}") # Log de erro com status e detalhes
        return None # Retorna None caso ocorra um erro
```

```Python
def save_to_s3(data, filename):
    try:
        # Obtém a data atual para criar a estrutura de diretórios com ano, mês e dia pra poder definir um caminho para salvar o arquivo no S3
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')

        # Cria/define um prefixo pro caminho no S3, organizado por ano, mês e dia
        prefix = f"Raw/API/Movies/{year}/{month}/{day}/"
        s3_key = f"{prefix}{filename}"

        # Salvar o arquivo JSON no S3
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=json.dumps(data)) # Converte os dados para JSON e salva
        print(f"Arquivo {s3_key} salvo com sucesso no S3.") # Log de confirmação de sucesso
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}") # Loga qualquer exceção que ocorra ao salvar no S3
```

```Python
def process_movies():
    page = 1 # Inicia na página 1 da API
    all_movies = [] # Lista que armazenará filmes antes de salvar em lotes de 100

    
    while page <=67: # Limita as páginas a 67 para evitar chamadas em excesso
        movies_data = get_movies(page) # Chama a função pra obter os dados da API
        if not movies_data:  # Se não tiver dados, sai do loop
        	break
        
        results = movies_data.get('results', []) # Extrai a lista de filmes, ou uma lista vazia caso não exista
        
        if not results: # Se a lista de resultados estiver vazia, interrompe o loop
            break
        
        all_movies.extend(results) # Adiciona os filmes da página atual à lista all_movies
        
        # Se tiver 100 ou mais filmes, salva e reseta a lista
        if len(all_movies) >= 100:
            filename = f"movies_page_{page}.json" # Define o nome do arquivo
            save_to_s3(all_movies, filename) # Salva o lote de filmes no S3
            all_movies = [] # Reseta a lista para os próximos 100 filmes
        page += 1 # Passa pra próxima página

    # Se tiver filme depois do loop, salva no S3
    if all_movies:
        filename = f"movies_page_{page}.json" # Define o nome do último arquivo
        save_to_s3(all_movies, filename)  # Salva o restante dos filmes no S3

if __name__ == "__main__":
    process_movies() # Chama a função principal para processar filmes da API
```

## Código Spark

### CSV

```Python
import sys # Acesso a algumas variáveis usadas ou mantidas pelo Python
from awsglue.transforms import * # Importa todas as funções do módulo de transformações do AWS Glue, que possui operações para manipulação de dados
from awsglue.utils import getResolvedOptions # Importa a função getResolvedOptions do módulo utils do AWS Glue, que é usada para obter argumentos passados para o job
from pyspark.context import SparkContext # Importa a classe SparkContext, que é a entrada principal para a funcionalidade do Spark
from awsglue.context import GlueContext # Importa a classe GlueContext, que fornece uma interface de nível mais alto para o AWS Glue, permitindo integração com o Spark
from awsglue.job import Job # Importa a classe Job, que representa um job do Glue e fornece métodos para inicializar e finalizar o job
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType # Importa os tipos de dados do PySpark para definir o esquema do DataFrame

## @params: [JOB_NAME]  # Comentário que indica que o job espera um parâmetro chamado JOB_NAME ao ser executado.
args = getResolvedOptions(sys.argv, ['JOB_NAME']) # Obtém os parâmetros passados pro job, especificamente o JOB_NAME, a partir da linha de comando
sc = SparkContext() # Cria uma instância do SparkContext, que é necessária para inicializar o Spark
glueContext = GlueContext(sc) # Cria uma instância do GlueContext, passando o SparkContext, para usar as funcionalidades do AWS Glue
spark = glueContext.spark_session # Obtém a sessão Spark do GlueContext, que é usada para trabalhar com DataFrames e RDDs
job = Job(glueContext) # Cria uma nova instância da classe Job, que representa o job do Glue.

job.init(args['JOB_NAME'], args) # Inicializa o job com o nome fornecido e os parâmetros obtidos anteriormente.

# Definindo o esquema para o DataFrame
schema_movies = StructType([
    # Define o esquema para o DataFrame de filmes, especificando os nomes das colunas e tipos
    StructField("id", IntegerType(), True),
    StructField("tituloPrincipal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notamedia", FloatType(), True)
])

schema_series = StructType([
    # Define o esquema para o DataFrame de séries, da mesma forma que para filmes.
    StructField("id", IntegerType(), True),
    StructField("tituloPrincipal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notamedia", FloatType(), True)
])

# Definir os caminhos da Raw Zone (origem) e Trusted Zone (destino)
raw_zone_path_movies = "s3://data-lake-flavia-passos/Raw/Local/CSV/Movies/"
# Caminho para a pasta onde estão armazenados os arquivos CSV de filmes na Raw Zone

raw_zone_path_series = "s3://data-lake-flavia-passos/Raw/Local/CSV/Series/"
# Caminho para a pasta onde estão armazenados os arquivos CSV de séries na Raw Zone

trusted_zone_path_movies = "s3://data-lake-flavia-passos/trusted/movies/"
# Caminho para a pasta onde os dados transformados de filmes serão armazenados na Trusted Zone

trusted_zone_path_series = "s3://data-lake-flavia-passos/trusted/series/"
# Caminho para a pasta onde os dados transformados de séries serão armazenados na Trusted Zone

# Definindo os DataFrames para ler os dados da Raw Zone
df_raw_movies = spark.read.format("csv").option("header", "true").schema(schema_movies).load(raw_zone_path_movies)
# Lê os arquivos CSV de filmes, especificando que o primeiro linha contém os cabeçalhos, usando o schema definido

df_raw_series = spark.read.format("csv").option("header", "true").schema(schema_series).load(raw_zone_path_series)
# Lê os arquivos CSV de séries, da mesma forma que para filmes

# Realizar as transformações necessárias (limpeza, padronização)
df_clean_movies = df_raw_movies.dropna(how="all") 
# Remove linhas do DataFrame de filmes que estão completamente vazias

df_clean_series = df_raw_series.dropna(how="all")
# Remove linhas do DataFrame de séries que estão completamente vazias

# Gravar os dados transformados na Trusted Zone em formato Parquet
df_clean_movies.write.mode("overwrite").format("parquet").save(trusted_zone_path_movies)
# Salva o DataFrame de filmes limpos na Trusted Zone no formato Parquet, sobrescrevendo os arquivos existentes.

df_clean_series.write.mode("overwrite").format("parquet").save(trusted_zone_path_series)
# Salva o DataFrame de séries limpos na Trusted Zone no formato Parquet, sobrescrevendo os arquivos existentes.

# Finalizar o job
job.commit()
# Finaliza o job, marcando-o como completo e garantindo que todas as operações sejam concluídas corretamente.
```

Este código configura um job no AWS Glue para ler arquivos CSV de filmes e séries de uma Raw Zone no Amazon S3, realiza limpeza de dados (removendo linhas vazias) e salva os dados processados em formato Parquet em uma Trusted Zone. O esquema para os dados é definido utilizando StructType e StructField, e o job é finalizado com um commit para garantir que todas as operações sejam registradas

### JSON

```Python
import sys # Acesso a algumas variáveis usadas ou mantidas pelo Python
from awsglue.transforms import * # Importa todas as funções do módulo de transformações do AWS Glue, que possui operações para manipulação de dados
from awsglue.utils import getResolvedOptions # Importa a função getResolvedOptions do módulo utils do AWS Glue, que é usada para obter argumentos passados para o job
from pyspark.context import SparkContext # Importa a classe SparkContext, que é a entrada principal para a funcionalidade do Spark
from awsglue.context import GlueContext # Importa a classe GlueContext, que fornece uma interface de nível mais alto para o AWS Glue, permitindo integração com o Spark
from awsglue.job import Job # Importa a classe Job, que representa um job do Glue e fornece métodos para inicializar e finalizar o job
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, MapType # Importa tipos de dados do PySpark para definir o schema do DataFrame, (tipos para arrays e mapas)
from pyspark.sql.functions import explode, col # Importa funções do PySpark, como explode (para transformar arrays em linhas) e col (para referenciar colunas)


## @params: [JOB_NAME]  # Comentário que indica que o job espera um parâmetro chamado JOB_NAME ao ser executado.
args = getResolvedOptions(sys.argv, ['JOB_NAME']) # Obtém os parâmetros passados pro job, especificamente o JOB_NAME, a partir da linha de comando
sc = SparkContext() # Cria uma instância do SparkContext, que é necessária para inicializar o Spark
glueContext = GlueContext(sc) # Cria uma instância do GlueContext, passando o SparkContext, para usar as funcionalidades do AWS Glue
spark = glueContext.spark_session # Obtém a sessão Spark do GlueContext, que é usada para trabalhar com DataFrames e RDDs
job = Job(glueContext) # Cria uma nova instância da classe Job, que representa o job do Glue.

job.init(args['JOB_NAME'], args) # Inicializa o job com o nome fornecido e os parâmetros obtidos anteriormente

# Definir os caminhos da Raw Zone (origem) e Trusted Zone (destino)
raw_zone_path_tmdb = "s3://data-lake-flavia-passos/Raw/API/Movies"
# Caminho para a pasta onde estão armazenados os arquivos JSON na Raw Zone do TMDB

trusted_zone_path_tmdb = "s3://data-lake-flavia-passos/Trusted/API/Movies/"
# Caminho para a pasta onde os dados transformados do TMDB serão armazenados na Trusted Zone

# Definir o esquema manualmente com base nos campos dos arquivos JSON
schema = StructType([
    # Define o esquema para o DataFrame, especificando os nomes das colunas e tipos
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("release_date", StringType(), True),
    StructField("genres", ArrayType(MapType(StringType(), StringType())), True),
    # 'genres' é um array de mapas, onde cada mapa contém pares chave-valor (string)
])

# Usar o schema definido ao carregar os dados JSON
df_raw_json = spark.read.format("json").schema(schema).load(raw_zone_path_tmdb)
# Lê os arquivos JSON usando o schema definido, especificando o caminho da Raw Zone

# Transformação: Extrair apenas os nomes dos gêneros
df_exploded = df_raw_json.withColumn("genre_name_exploded", explode(col("genres"))).select(
    # Usa explode para transformar o array de gêneros em linhas, criando uma nova coluna "genre_name_exploded".
    "*",  # Seleciona todas as colunas do DataFrame original.
    col("genre_name_exploded.name").alias("genre_name")  # Extrai o nome do gênero do mapa e renomeia a coluna.
)

# Remover a coluna temporária "genre_name_exploded" se ainda existir
df_clean_json = df_exploded.drop("genre_name_exploded").withColumnRenamed("original_title", "titulo")
# Remove a coluna temporária "genre_name_exploded" e renomeia a coluna "original_title" para "titulo".

# Salvar o DataFrame transformado na Trusted Zone em formato Parquet
df_clean_json.write.mode("overwrite").format("parquet").save(trusted_zone_path_tmdb)
# Salva o DataFrame limpo na Trusted Zone no formato Parquet, sobrescrevendo arquivos existentes.

job.commit()
# Finaliza o job, marcando-o como completo e garantindo que todas as operações sejam concluídas corretamente.
```

Este código configura um job no AWS Glue para ler arquivos JSON da Raw Zone no Amazon S3, realiza transformações para extrair nomes de gêneros e salva os dados processados em formato Parquet na Trusted Zone. O esquema para os dados é definido utilizando StructType, e a função explode é usada para transformar arrays em linhas, permitindo uma manipulação mais fácil dos dados. O job é finalizado com um commit para garantir que todas as operações sejam registradas.

# Evidências
As evidências do processamento e dos resultados estão incluídas neste repositório [Evidencias](./Evidencias)



