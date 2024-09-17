import boto3
import csv
from io import StringIO

# Configura uma sessão aws usando boto3 com um perfil sso, assim não precisa expor as credenciais, ele faz uma consulta(query) pra processar os dados diretamente no S3 (com S3 Select)
session = boto3.Session(profile_name='sso-session1') 
# Configurar o cliente S3 e usa pra acessar a AWS via SSO, interage com o serviço S3, incluindo a execução de consultas
s3 = session.client('s3')

# entre aspas simples são interpretados como valores literais
# entre aspas duplas são interpretados como objetos de banco de dados (referências de coluna ou tabela)
# group by, lenght, concat não são suportados pelo s3select 
def execute_s3_select(bucket_name, key):
    query = """
    SELECT *
    FROM s3object 
    """

    response = s3.select_object_content(
        Bucket=bucket_name,
        Key=key,
        ExpressionType='SQL',
        Expression=query,
        InputSerialization={'CSV': {'FileHeaderInfo': 'USE', 'FieldDelimiter': ';'}},
        OutputSerialization={'CSV': {}}
    )
    records = []
    for event in response['Payload']:
        if 'Records' in event:
            records.append(event['Records']['Payload'].decode('utf-8'))
        elif 'End' in event:
            break
    return ''.join(records)

def process_results(results):
    lines = results.strip().split('\n')

    headers = lines[0].split(',')
    
    data = []
    for line in lines[1:]:
        data.append(line.split(','))
    
    totals = [0] * (len(headers) - 1) 

    for row in data:
        try:
            if row[0].strip() == 'Total ':
                continue
            for i in range(1, len(row)):
                totals[i - 1] += float(row[i].replace('.', '').replace(',', '.'))
        except ValueError:
            print(f"Erro ao processar a linha: {row}")

    print(f"Total de exames: {totals}")
    
    num_rows = len(data) - 1 
    if num_rows > 0:
        averages = [total / num_rows for total in totals]
    else:
        averages = [0] * len(totals)

    print(f"Média de exames em janeiro: {averages[0]:.2f}")
    print(f"Média de exames em fevereiro: {averages[1]:.2f}")
    print(f"Média de exames em março: {averages[2]:.2f}")
    print(f"Média de exames em abril: {averages[3]:.2f}")

bucket_name = 'desafio-compass'
file_key = 'exames_laboratoriais-janeiro-abril2024.csv'
results = execute_s3_select(bucket_name, file_key)
print("Resultado da consulta SQL:")
print(results)
process_results(results)





