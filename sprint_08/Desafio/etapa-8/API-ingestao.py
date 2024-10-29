import os
import json
import boto3
import requests
from dotenv import load_dotenv
from datetime import datetime

# Carregar o arquivo .env
load_dotenv()

# Acessar as chaves da API
tmdb_api_key = os.getenv('TMDB_API_KEY')
S3_BUCKET = 'data-lake-flavia-passos'
BASE_URL = 'https://api.themoviedb.org/3'

# Configurar cliente do S3
session = boto3.Session(profile_name='AdministratorAccess-529088293312')
s3 = session.client('s3')

def get_movies(page):
    url = f"{BASE_URL}/movie/upcoming?api_key={tmdb_api_key}&language=pt-BR&page={page}"
    response = requests.get(url)
    
    print(f"URL: {url}")  # Log da URL
    print(f"Status Code: {response.status_code}")  # status da resposta
    print(f"Response Text: {response.text}")  # Log do corpo da resposta
    
    if response.status_code == 200:
    	movies_data = response.json()
    	print(movies_data)
    	return movies_data
    else:
        print(f"Erro ao buscar filmes: {response.status_code} - {response.text}")
        return None
        

def save_to_s3(data, filename):
    try:
        # Definir um caminho para salvar o arquivo no S3
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')

        # Definir o prefixo para a pasta
        prefix = f"Raw/API/Movies/{year}/{month}/{day}/"
        s3_key = f"{prefix}{filename}"

        # Salvar o arquivo no S3
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=json.dumps(data))
        print(f"Arquivo {s3_key} salvo com sucesso no S3.")
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}")
        
def process_movies():
    page = 1
    all_movies = []
    
    while page <=67:
        movies_data = get_movies(page)
        if not movies_data:
        	break
        
        results = movies_data.get('results', [])
        
        if not results:
            break
        
        all_movies.extend(results)
        
        # Se já temos 100 filmes, salva e reseta a lista
        if len(all_movies) >= 100:
            filename = f"movies_page_{page}.json"
            save_to_s3(all_movies, filename)
            all_movies = []
        page += 1

    # Salva os filmes restantes, se houver
    if all_movies:
        filename = f"movies_page_{page}.json"
        save_to_s3(all_movies, filename)

if __name__ == "__main__":
    process_movies()  # Processar filmes da API

