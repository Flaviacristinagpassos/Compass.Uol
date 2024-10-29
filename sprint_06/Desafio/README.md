# Desafio de Construção de um Data Lake para Filmes e Séries <img align="center" width=80 height=70 src="https://files.cdata.com/media/media/izvfwdfj/what-is-a-data-lake.png" />

## Introdução
Este desafio acadêmico tem como objetivo a construção de um Data Lake que armazene e processe dados de filmes e séries, utilizando diferentes fontes de dados. O processo inclui ingestão, armazenamento, processamento e consumo de dados, utilizando arquivos CSV e dados da API do TMDB. O desafio é dividido em etapas, sendo a primeira, a ingestão de arquivos CSV para a camada "Raw" do Data Lake. O Data Lake será utilizado para análise e visualização dos dados, respondendo a perguntas analíticas previamente definidas.

## Etapas do Desafio
1. **Ingestão dos Dados**: Os dados serão ingeridos a partir de duas fontes principais:
   - Arquivo CSV contendo informações de filmes e séries.
   - API do TMDB, para enriquecer as informações com dados adicionais.

2. **Armazenamento e Padronização**: Os dados ingeridos serão armazenados na camada "Raw" do Data Lake, em sua forma original. Em seguida, serão processados e padronizados para serem movidos para a camada "Staging", onde estarão disponíveis em um formato mais eficiente (Parquet ou ORC) e catalogados no AWS Glue.

3. **Processamento com Apache Spark**: Os dados na camada "Staging" serão processados e transformados utilizando o Apache Spark, com o objetivo de padronizar e preparar os dados para análises futuras. Os dados processados serão então movidos para a camada "Curated".

4. **Modelo de Dados Dimensional**: Um modelo de dados dimensional será construído para permitir análises eficientes. O modelo será baseado em dimensões como diretores, gêneros e nacionalidades, e fatos relacionados a avaliações e classificações de filmes e séries.

5. **Consumo de Dados e Visualização**: A última camada do Data Lake (Curated) será utilizada para o consumo de dados através de dashboards analíticos. As análises incluirão comparações de avaliações entre diferentes plataformas (TMDB e IMDB), nacionalidades de diretores e outros insights relevantes.

## Perguntas de Análise
Com base na exploração inicial dos dados, as seguintes questões serão respondidas:
1. **Quantos filmes de Drama e Romance existem?**
      - Total de filmes classificados como Drama ou Romance

2. **Quantos títulos únicos de filmes pertencem ao gênero Drama?**
      - Contar o número de títulos únicos de filmes no genêro Drama

3. **Quantos títulos únicos de filmes pertencem ao gêneros Romance?**
      - Contar o número de títulos únicos no gênero Romance,

Essas questões guiarão a análise e a construção dos dashboards analíticos na fase final do desafio.

Com as perguntas analíticas definidas, o próximo passo é iniciar a primeira entrega do desafio, que envolve a ingestão batch dos arquivos CSV para a raw zone no Amazon S3. O objetivo é criar um código Python para ler os arquivos movies.csv e series.csv, sem realizar filtragem, e carregá-los para um bucket S3 seguindo a estrutura de diretórios que foi especificada no enunciado do desafio. Isso será feito dentro de um container Docker.

<br>

# Etapas da Entrega 1: Ingestão Batch de CSV

A primeira entrega do desafio envolve a ingestão dos arquivos CSV contendo dados de filmes e séries para a raw zone do Data Lake no Amazon S3

### 1. Estrutura dos Arquivos CSV
Os arquivos CSV utilizados são:
- `movies.csv`: Contém dados sobre filmes, incluindo título, ano de lançamento, gênero, e nota média
- `series.csv`: Contém dados sobre séries, com informações semelhantes, além de colunas específicas sobre os personagens

### 2. Estrutura do Data Lake

O Data Lake segue a seguinte estrutura para armazenar os dados na raw zone:

```bash
<nome-do-bucket>/<camda-de-armazenamento>/<origem-do-dado>/<formato-do-dado>/</tipo-do-dado>/<ano>/<mês>/<dia>/<arquivo>.csv

<nome-do-bucket>/Raw/Local/CSV/<tipo-do-dado>/<ano>/<mês>/<dia>/<arquivo>.csv
```

```bash
data-lake-flavia-passos/Raw/Local/CSV/Movies/2024/09/30/movies.csv 
data-lake-flavia-passos/Raw/Local/CSV/Series/2024/09/30/series.csv
```

### 3. Código Python de Ingestão (ingestao.py)

O script Python desenvolvido faz a ingestão dos arquivos CSV para o S3 utilizando a biblioteca boto3. O código lê os arquivos `movies.csv` e `series.csv` e os faz upload para o bucket definido.

```python
import os
import boto3
from datetime import datetime

def upload_to_s3(file_path, bucket_name, data_type):
    s3_client = boto3.client('s3')
    
    # Extrair a data atual
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # Definir o caminho S3
    file_name = os.path.basename(file_path)
    s3_key = f"Raw/Local/CSV/{data_type}/{year}/{month}/{day}/{file_name}"

    try:
        # Fazer upload do arquivo
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Upload bem-sucedido: {file_name} para {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload de {file_name}: {e}")

def process_files(bucket_name):
    csv_files = {
        "Movies": "/home/nave/Área de Trabalho/projeto-data-lake/csv/movies.csv",
        "Series": "/home/nave/Área de Trabalho/projeto-data-lake/csv/series.csv"
    }

    for data_type, file_path in csv_files.items():
        if os.path.exists(file_path):
            upload_to_s3(file_path, bucket_name, data_type)
        else:
            print(f"Arquivo não encontrado: {file_path}")

if __name__ == "__main__":
    bucket_name = "data-lake-flavia-passos"
    process_files(bucket_name)
```
<br>

### 4. Explicação do Código

```Python
#Importa o módulo os, que permite a manipulação de arquivos e diretórios no sistema operacional
import os 

#Importa o módulo boto3, a biblioteca oficial da AWS para interagir com seus serviços, como o S3
import boto3 

#Importa a classe datetime, que será usada para obter a data e hora atuais
from datetime import datetime  
```

```Python
#Define uma função chamada upload_to_s3, que tem como parâmetros o caminho do arquivo (file_path), o nome do bucket S3 (bucket_name), e o tipo de dado (data_type), que pode ser 'Movies' ou 'Series'
def upload_to_s3(file_path, bucket_name, data_type): 

#Cria um cliente S3 usando a biblioteca boto3 para interagir com o serviço Amazon S3
      s3_client = boto3.client('s3') 
```

```Python
now = datetime.now() #Vai obter data e hora atuais.
year = now.strftime('%Y') #Extrai o ano da data atual no formato YYYY
month = now.strftime('%m'): #Extrai o mês da data atual no formato MM
day = now.strftime('%d'): #Extrai o dia da data atual no formato DD
```

```Python
#Extrai o nome do arquivo (por exemplo, movies.csv) a partir do caminho completo do arquivo.
file_name = os.path.basename(file_path)

#Define o caminho para onde o arquivo será enviado no S3, criando um diretório com base no tipo de dado (Movies ou Series) e na data (ano, mês, dia)
s3_key = f"Raw/Local/CSV/{data_type}/{year}/{month}/{day}/{file_name}" 
```

```Python
try: #Inicia um bloco try para capturar e tratar exceções

      #Faz o upload do arquivo localizado em file_path para o bucket S3 especificado por bucket_name, no caminho definido pela variável s3_key.
      s3_client.upload_file(file_path, bucket_name, s3_key)

      #Vai printar uma mensagem de sucesso indicando que o arquivo foi carregado com êxito para o bucket S3.
      print(f"Upload bem-sucedido: {file_name} para {bucket_name}/{s3_key}") 
```

```Python
#Captura qualquer exceção que possa ocorrer durante o upload do arquivo para o S3
except Exception as e: 

      #E printar uma mensagem de erro com o nome do arquivo e a descrição da exceção capturada
      print(f"Erro ao fazer upload de {file_name}: {e}"): 
```

```Python
#Definir uma função chamada process_files que recebe o nome do bucket S3 como parâmetro que vai ser responsável por processar vários arquivos CSV
def process_files(bucket_name): 

#Um dicionário que mapeia tipos de dados (Movies e Series) pro caminho absoluto dos arquivos CSV correspondentes
    csv_files = {
      "Movies": "/home/nave/Área de Trabalho/projeto-data-lake/csv/movies.csv",
      "Series": "/home/nave/Área de Trabalho/projeto-data-lake/csv/series.csv"
    }
```

```Python
#Começa um laço for que itera sobre os itens no dicionário csv_files. Pra cada item, o data_type será 'Movies' ou 'Series', e file_path será o caminho do arquivo correspondente
    for data_type, file_path in csv_files.items():

      #Verifica se o arquivo existe nesse caminho que foi especificado
        if os.path.exists(file_path):
            #Se o arquivo existir, ele chama a primeira função 'upload_to_s3' para fazer o upload pro S3
            upload_to_s3(file_path, bucket_name, data_type)
      #Se não, printa uma mensagem de erro informando que o arquivo não foi encontrado.
        else:
            print(f"Arquivo não encontrado: {file_path}")
```

```Python
#Verifica se o script ta sendo executado diretamente, e não importado como módulo
if __name__ == "__main__":
      #Define o nome do bucket S3 onde os arquivos vão ser enviados
      bucket_name = "data-lake-flavia-passos"
      #Chama a segunda função 'process_files', passando o nome do bucket para iniciar o processo de upload dos arquivos CSV pro S3
      process_files(bucket_name)
```

### 5. Problema ao Utilizar Docker
Inicialmente, tentei executar o código de ingestão dentro de um container Docker com o seguinte comando:

```bash
docker run --rm -v ~/.aws:/root/.aws -v ~/Área\ de\ Trabalho/projeto-data-lake/csv:/csv ingestao-data-lake:latest
```

No entanto, enfrentei um erro relacionado à chave de acesso AWS (InvalidAccessKeyId), indicando que a chave de acesso configurada não estava correta no ambiente do container. Após verificar as configurações do AWS CLI, a ingestão foi realizada manualmente utilizando o script Python localmente, sem o uso do Docker.
Porém depois de arrumar as credenciais consegui fazer a ingestão com Docker

### 6. Solução Alternativa
Devido aos problemas com as chaves de acesso dentro do container, a ingestão foi feita diretamente no ambiente local, utilizando o script Python. Os arquivos CSV foram enviados corretamente para o bucket S3.
Acabei usando essa solução antes de testar com o Docker depois.

[Pasta Evidencias](./Evidencias)


<br>

# Próximas Etapas

1. **Ingestão de Dados da API do TMDB** 
      - Na próxima etapa, será implementada a ingestão de dados diretamente da API do TMDB para complementar os dados dos arquivos CSV
2. **Processamento de Dados**
      - Após a ingestão, os dados serão processados para padronizar o formato e movidos para a próxima camada do Data Lake
3. **Modelo de Dados Dimensional**
      - Definição de um modelo de dados dimensional, com base nas questões analíticas estabelecidas, para guiar a próxima fase de processamento e análise dos dados
4. **Análise Final** 
      - O consumo dos dados será feito através de dashboards que responderão às perguntas analíticas definidas no início do desafio.

<br>

# Conclusão
Esta entrega focou na ingestão batch dos arquivos CSV para a raw zone do Data Lake. A partir daqui, teremos avanço para o processamento e análise de dados, garantindo que os dados estejam organizados e preparados para o consumo na última camada do Data Lake.