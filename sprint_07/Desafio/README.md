# Projeto Data Lake - Drama e Romance

#### Este projeto é parte 2 de um desafio para a construção de um Data Lake utilizando serviços da AWS. Ele envolve as etapas de ingestão, armazenamento, processamento e consumo de dados. O projeto foi dividido em duas partes:

- Ingestão de dados batch de arquivos CSV.
- Ingestão de dados via API do TMDB.


# 1. Etapas da Entrega parte 2: Ingestão de Dados via API (TMDB)

### 2. Definição dos Requisitos
A segunda parte do desafio envolve a ingestão de dados complementares de filmes e séries via API do TMDB.

Os dados estão no S3 em formato JSON, com no máximo 100 registros por arquivo.

### 3. Configuração do Arquivo .env

Criamos um arquivo .env contendo as chaves de acesso para a API do TMDB e as credenciais AWS necessárias para o S3.

foi usado o arquivo .env ao inves do AWS Secrets Manager, pela questao de custo, porem particularmente eu prefiria ter usado o secret management mas nao tinha necessidade.

## 4. Configuração do Ambiente para a Função Lambda e Ingestão de Dados
Embora o uso de IAM Roles seja uma prática recomendada para acessar serviços AWS como o S3, optei por utilizar as variáveis de ambiente com criptografia habilitada. Isso foi feito para garantir que os dados sensíveis, como as chaves de API e credenciais AWS, fossem protegidos tanto em repouso quanto em trânsito.


- **Criptografia em Trânsito** 
    - Assegurar que as variáveis de ambiente fossem criptografadas durante a transmissão entre o AWS Lambda e os serviços da AWS. Isso oferece uma camada adicional de proteção para dados sensíveis, especialmente importante para proteger dados sensíveis como chaves de acesso. Como a AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.


- **Restrições em Variáveis de Ambiente Reservadas** 
    - Importante observar que algumas variáveis de ambiente, como AWS_REGION, AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY, são consideradas chaves reservadas e não devem ser usadas como variáveis de ambiente em funções Lambda. Embora seja possível definir variáveis de ambiente com esses nomes, é recomendado usar IAM Roles para conceder permissões à função Lambda. 
    Em vez de depender apenas das variáveis de ambiente para acessar o S3, foi configurado um usuário IAM com as permissões adequadas. Isso garantiu que a função Lambda tivesse os privilégios necessários para acessar o S3 e realizar o upload dos arquivos JSON, preservando uma estrutura de segurança sólida.


### Instalação de Dependências (pra carregar o zip) e Criação de Layer
![Evidencias] (.sprint_07/Evidencias/Dependencia-camada.png)

Como a função Lambda precisa de algumas bibliotecas para realizar as tarefas, para preparar o ambiente e criar uma Layer que contenha as dependências necessárias foi feito:

1. **Configurar um ambiente virtual Python para isolar as dependências do projeto**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Instalar bibliotecas essenciais para que o código possa interagir com a API do TMDB e com o S3**
```bash
pip install boto3 tmdbv3api requests
```
boto3: para interagir com o AWS S3
tmdbv3api: para interagir com a API do TMDB
requests: para fazer chamadas HTTP (embora a biblioteca tmdbv3api já faça isso)


3.**Gerar o Arquivo da Layer**
- Criar a Layer que será utilizada no AWS Lambda, seguimos estes passos
- Criar uma pasta chamada python para armazenar as bibliotecas
- Copiar as dependências instaladas para essa pasta
- Compactar a pasta python em um arquivo ZIP, que foi utilizado como Layer na função Lambda

```bash
mkdir python
cp -r venv/lib/python3.8/site-packages/* python/
zip -r9 layer.zip python
```


## 5. Criação do Código de Ingestão via API

Foi criado o arquivo API-ingestao.py para realizar as chamadas à API do TMDB e salvar os dados no S3.
A biblioteca requests foi usada para fazer as requisições à API, e o boto3 para gravar os dados no S3

```Python
import os
import json
import boto3
import requests
from dotenv import load_dotenv
from datetime import datetime
from tmdbv3api import TMDb, Movie

# Carregar o arquivo .env
load_dotenv()

# Obter chaves da API e credenciais AWS
tmdb_api_key = os.getenv('TMDB_API_KEY')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

# Configurar a API do TMDB
tmdb = TMDb()
tmdb.api_key = tmdb_api_key

# Teste básico para verificar a API do TMDB
movie = Movie()
try:
    popular_movies = movie.popular()
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

    # Buscar dados de séries
    series_params = {'language': 'pt-BR', 'page': 1}
    series_data = fetch_tmdb_data('tv/popular', series_params)

    if series_data:
        upload_to_s3(series_data, bucket_name, 'Series')

if __name__ == "__main__":
    bucket_name = "data-lake-flavia-passos"
    process_api_data(bucket_name)
```

# 6. Explicação do Código 

```Python
import os  # Interagir com o sistema operacional e acessar variáveis de ambiente
import json  # Facilita trabalhar com dados no formato JSON
import boto3  # Interagir com os serviços da AWS (S3)
import requests  # Para fazer requisições HTTP à API do TMDB
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env
from datetime import datetime  # Usado para obter a data e hora atuais
from tmdbv3api import TMDb, Movie  # Biblioteca para interagir com a API do TMDB, facilitando a busca por dados de filmes

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv() 

# Obter a chave da API do TMDB do arquivo .env
tmdb_api_key = os.getenv('TMDB_API_KEY')

# Obter as credenciais da AWS do arquivo .env
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Obter a região da AWS do arquivo .env
aws_region = os.getenv('AWS_REGION')

# Configurar a API do TMDB usando a chave da API
tmdb = TMDb()
tmdb.api_key = tmdb_api_key

# Teste básico para verificar se a chave da API está funcionando corretamente
movie = Movie()

try:
    # Faz uma chamada pra obter filmes populares através da API do TMDB
    popular_movies = movie.popular()
    # Printa os títulos dos filmes populares
    print(popular_movies)
    # Itera sobre os resultados da API e imprime os títulos dos filmes populares
    for m in popular_movies.results:
        print(m.title)
# Se tiver erro na chamada da API, printa uma mensagem de erro   
except Exception as e:
    print(f"Erro na API: {e}")

# Configura o cliente do AWS S3 usando as credenciais da AWS
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)

```
<br>

```Python
# Função pra buscar dados da API do TMDB, com base no endpoint e nos parâmetros fornecidos
def fetch_tmdb_data(endpoint, params):
    base_url = "https://api.themoviedb.org/3"  # URL base da API do TMDB
    headers = {'Authorization': f'Bearer {tmdb_api_key}'}  # Headers para autenticação com a chave da API
    # Fazer a requisição GET para o endpoint da API com os parâmetros fornecidos
    response = requests.get(f"{base_url}/{endpoint}", params=params)

    # Verifica se a resposta da API foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Retornar os dados da API em formato JSON
        return response.json()
    else:
        # Se a resposta não foi bem-sucedida, printa uma mensagem de erro
        print(f"Erro na API: {response.status_code}")
        return None
```
<br>

```Python
# Função que faz upload de um arquivo JSON para o S3, usando o cliente boto3
def upload_to_s3(data, bucket_name, data_type):
    # Obter a data e hora atuais
    now = datetime.now()
    # Extrair o ano, mês e dia atuais
    year = now.strftime('%Y') # Formato YYY
    month = now.strftime('%m') # Formato MM
    day = now.strftime('%d') # Formato DD

    # Cria o nome do arquivo JSON com base na hora atual
    file_name = f"{data_type}_{now.strftime('%H%M%S')}.json"

    # Define o caminho completo do arquivo no S3, organizando por tipo de dados, ano, mês e dia
    s3_key = f"Raw/API/{data_type}/{year}/{month}/{day}/{file_name}"

    # Tenta fazer o upload do arquivo JSON pro S3
    try:
        # Converte os dados em formato JSON e faz o upload para o S3 usando o método `put_object()`
        s3_client.put_object(
            Body=json.dumps(data),  # Converter os dados em uma string JSON
            Bucket=bucket_name,  # Nome do bucket S3 onde o arquivo será armazenado
            Key=s3_key  # Caminho do arquivo dentro do bucket
        )
        # Printa uma mensagem de sucesso indicando que o upload foi concluído com sucesso
        print(f"Upload bem-sucedido: {file_name} para {bucket_name}/{s3_key}")
    except Exception as e:
        # Se houver erro no upload, printa uma mensagem de erro
        print(f"Erro ao fazer upload: {e}")
```
<br>

```Python
# Função principal para buscar e armazenar dados pro S3 de filmes e séries da API do TMDB
def process_api_data(bucket_name):
    # Definir os parâmetros para a busca de filmes populares incluindo o idioma e a página de resultados
    movie_params = {'language': 'pt-BR', 'page': 1}    
    # Chama a função `fetch_tmdb_data()` para buscar os filmes populares
    movie_data = fetch_tmdb_data('movie/popular', movie_params)

    # Se os dados de filmes forem encontrados, faz upload pro S3
    if movie_data:
        upload_to_s3(movie_data, bucket_name, 'Movies')

    # Definir os parâmetros para a busca de séries populares (idioma e página), parecido com filmes
    series_params = {'language': 'pt-BR', 'page': 1}
    # Chama a função `fetch_tmdb_data()` pra buscar as séries populares
    series_data = fetch_tmdb_data('tv/popular', series_params)

    # Se os dados de séries forem encontrados, fazer upload para o S3
    if series_data:
        upload_to_s3(series_data, bucket_name, 'Series')

# Ponto de entrada do script, que é executado quando o arquivo é chamado diretamente
if __name__ == "__main__":
    # Nome do bucket S3 onde os dados serão armazenados
    bucket_name = "data-lake-flavia-passos"
    # Chama a função principal pra buscar e processar os dados da API
    process_api_data(bucket_name)
```

## Persistência dos Dados no S3
A cada requisição, os dados são salvos no diretório Raw/API/ do bucket S3
Os dados foram divididos em arquivos com no máximo 100 registros para manter a organização e facilitar o processamento posterior


## Parte 3: (Em Andamento) - Processamento e Agregação
Agora trabalhando na definição de questões analíticas e iniciando o processamento dos dados para gerar insights sobre filmes e séries da categoria Drama e Romance. Essa parte envolve o uso de serviços da AWS como AWS Glue e AWS Athen

Desempenho no Athena: Houve desafios relacionados ao tempo de execução no AWS Athena, que estão sendo analisados.

## Ferramentas Utilizadas
- AWS S3: Armazenamento dos dados CSV e JSON;
- AWS Lambda: Ingestão de dados via API do TMDB;
- Docker: Execução do código localmente;
- Boto3: Interação com AWS S3 e outros serviços AWS;
- Requests: Biblioteca Python para requisições HTTP à API do TMDB;
- TMDbv3api: Biblioteca Python para trabalhar com a API do TMDB.

# Conclusão
Neste desafio, implementamos um Data Lake usando o Amazon S3, ingerindo dados via API do TMDB com AWS Lambda. Utilizamos boas práticas de segurança, como criptografia de variáveis de ambiente e IAM Roles. Enfrentamos e resolvemos desafios técnicos, como o gerenciamento de dependências e organização dos dados em formato JSON.
