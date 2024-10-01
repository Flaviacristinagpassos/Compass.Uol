import os
import boto3
from datetime import datetime


# Função para enviar arquivo pro S3
def upload_to_s3(file_path, bucket_name, data_type):
    s3_client = boto3.client('s3')
    
    # Extrair a data atual para o padrão de diretório
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # Definir o caminho S3 para onde o arquivo será enviado
    file_name = os.path.basename(file_path)
    s3_key = f"Raw/Local/CSV/{data_type}/{year}/{month}/{day}/{file_name}"

    try:
        # Enviar o arquivo para o bucket S3
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Upload bem-sucedido: {file_name} para {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload de {file_name}: {e}")

# Função principal para processar os arquivos CSV
def process_files(bucket_name):
    # Definir o caminho dos arquivos locais
    csv_files = {
    	"Movies": "/home/nave/Área de Trabalho/projeto-data-lake/csv/movies.csv",
        "Series": "/home/nave/Área de Trabalho/projeto-data-lake/csv/series.csv"
    }

    # Enviar cada arquivo para o S3
    for data_type, file_path in csv_files.items():
        if os.path.exists(file_path):
            upload_to_s3(file_path, bucket_name, data_type)
        else:
            print(f"Arquivo não encontrado: {file_path}")

if __name__ == "__main__":
    # Nome do bucket S3
    bucket_name = "data-lake-flavia-passos"
    
    # Processar os arquivos
    process_files(bucket_name)

