import os # permite interagir com o sistema operacional e acessar as variaveis de ambiente
import json
import boto3
import requests
from dotenv import load_dotenv # pra carregar as variaveis de ambiente de um arquivo .env
from datetime import datetime
from tmdbv3api import TMDb, Movie

# Carregar o arquivo .env por padrao, pra que estejam disponíveis no ambiente de execução do Python
load_dotenv() 

# Acessar as chaves da API

# Obter o valor da variável de ambiente TMDB_API_KEY (a chave da API do TMDB) a partir do sistema, que foi carregada pelo .env
tmdb_api_key = os.getenv('TMDB_API_KEY')

# Obter o valor da chave de acesso da AWS
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')

# Obter o valor da chave secreta de acesso da AWS.
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Obter o valor da região AWS
aws_region = os.getenv('AWS_REGION')

# Configurar a API do TMDB
tmdb = TMDb()
tmdb.api_key = tmdb_api_key

# Teste básico para verificar a chave da API
movie = Movie()

try:
    popular_movies = movie.popular()
    print(popular_movies)
    for m in popular_movies.results:
        print(m.title)
except Exception as e:
    print(f"Erro na API: {e}")


# Configurar cliente do S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)
                         
                         
# Função para buscar dados de filmes ou séries do TMDB
def fetch_tmdb_data(endpoint, params):
    base_url = "https://api.themoviedb.org/3"
    headers = {'Authorization': f'Bearer {tmdb_api_key}'}
    response = requests.get(f"{base_url}/{endpoint}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na API: {response.status_code}")
        return None

# Função para enviar arquivo JSON para o S3
def upload_to_s3(data, bucket_name, data_type):
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # Definir o caminho no S3
    file_name = f"{data_type}_{now.strftime('%H%M%S')}.json"
    s3_key = f"Raw/API/{data_type}/{year}/{month}/{day}/{file_name}"

    # Enviar os dados para o S3
    try:
        s3_client.put_object(
            Body=json.dumps(data),
            Bucket=bucket_name,
            Key=s3_key
        )
        print(f"Upload bem-sucedido: {file_name} para {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")

# Função principal para buscar e armazenar dados de filmes/séries
def process_api_data(bucket_name):
    movie_params = {'language': 'pt-BR', 'page': 1}
    movie_data = fetch_tmdb_data('movie/popular', movie_params)

    if movie_data:
        upload_to_s3(movie_data, bucket_name, 'Movies')

    # Fazer o mesmo para séries
    series_params = {'language': 'pt-BR', 'page': 1}
    series_data = fetch_tmdb_data('tv/popular', series_params)

    if series_data:
        upload_to_s3(series_data, bucket_name, 'Series')

if __name__ == "__main__":
    bucket_name = "data-lake-flavia-passos"
    process_api_data(bucket_name)
