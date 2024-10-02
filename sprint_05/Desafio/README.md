# Neste Desafio foi proposto:

Praticar conhecimentos de nuvem AWS aprendidos na Sprint 5

Como utilizei a AWS SSO (e boto3) que já gerencia as minhas credencias, não utilizei '.env' e 'dotenv'  
E já que eu não utilizei arquivos que tivessem informações sensíveis, que seria o caso de ter usado '.env' e 'dotenv', não preciso adicionar ao .gitignore

requirements.txt: Ele não é necessário para usar o AWS CLI diretamente, mas se você estiver criando scripts Python que usam o SDK da AWS (boto3), você incluiria boto3 no requirements.txt. Ele serve para gerenciar dependências em projetos Python.

### O código realiza consulta ao S3 usando S3 Select, faz o processamendo dos resultados e faz o cálculo de totais e médias

## 1. importando as bibliotecas necessárias

```Python
import boto3 # Usado para interagir com o Amazon S3
import csv # Pra processar o conteúdo CSV
from io import StringIO # manipular o conteúdo do CSV em memória
```

## 2. 
O código , faz uma consulta(query) pra processar os dados diretamente no s3 (com s3 select).

```Python
# Configura uma sessão aws usando boto3 com um perfil sso, assim não precisa expor as credenciais, ele faz uma consulta(query) pra processar os dados diretamente no S3 (com S3 Select)
session = boto3.Session(profile_name='sso-session1') 
s3 = session.client('s3') # Configurar o cliente S3 e usa pra acessar a AWS via SSO, interage com o serviço S3, incluindo a execução de consultas
```

## 3. 

```Python
def execute_s3_select(bucket_name, file_key): # Define a função que recebe o nome do bucket e a chave csv
    query = """ # Define uma consulta SQL
    SELECT * # e seleciona todos(*) os dados 
    FROM S3Object # Do arquivo S3
    """
    # Método do API S3 que executa o S3 Select pra ler e processar o arquivo csv
    response = s3.select_object_content( 
        Bucket=bucket_name, # Nome do bucket onde onde o arquivo csv ta armazenado
        Key=file_key, # Chave do objeto (nome do arquivo CSV) dentro do bucket
        ExpressionType='SQL', # Define que a expressão é uma consulta SQL
        Expression=query, # A consulta SQL que vai ser executada no arquivo CSV
```

```Python
        # Como os dados do arquivo CSV devem ser interpretados pelo S3 Select
        InputSerialization={'CSV': {'FileHeaderInfo': 'USE', 'FieldDelimiter': ';'}}, 
        # Formato de entrada CSV
        # Primeira linha do CSV deve ser um cabeçalho e contém os nomes das colunas, 
        # E um delimitador de campos que é o ponto e vírgula
        # Quando o arquivo CSV utiliza ponto e vírgula como separador de colunas, ao invés da vírgula padrão, é preciso usar um delimitador
        OutputSerialization={'CSV': {}} # Define o formato da saída da consulta, que é CSV
    )

    # Cria uma lista vazia que vai ser usada pra armazenar os dados de cada registro retornado pela operação do S3 Select
    records = [] 

    # Percorre cada item na "carga útil" da resposta do select_object...
    for event in response['Payload']: 

    # Cada evento pode ter diferentes tipos de dados
    # Verifica se o evento atual tem a chave 'Records', isso indica que o evento possui dados de registro
        if 'Records' in event: 

            # Se tiver, ele vai extrair o 'Payload' dos registro que ta no formato binário
            # Decodifica o 'Payload' pra string usando utd-8 
            # E adiciona a string decodificada na lista 'records'
            records.append(event['Records']['Payload'].decode('utf-8'))

        # Verifica se o evento possui a chave 'END' que é o que indica o final da transmissão de dados
        # E o looop encerra com um break
        elif 'End' in event:
            break

    # Quando o loop acaba, a lista records tem todas as partes dos registros que foram coletados
    # Concatena todas as partes em uma só string que é retornada pela função
    return ''.join(records)
```

## 4. 

```Python
def process_results(results):
    # Remove os espaços em branco do início e do fim da string 'results' e divide a string em uma lista de linhas, usando o caractere '\n' como delimitador
    # Cada linha representa um registro (uma linha do CSV)
    lines = results.strip().split('\n')
    
    # Remove o cabeçalho
    # Pega a primeira linha, que contém os cabeçalhos do CSV e divide em uma lista, usando a vírgula como delimitador
    headers = lines[0].split(',')
    
    # Dados do CSV
    # Inicializa uma lista vazia chamada `data` que vai armazenar as linhas de dados do CSV sem o cabeçalho
    data = []

    # Percorre as linhas do CSV, começando da segunda linha (ignorando o cabeçalho)
    for line in lines[1:]:

        # Divide cada linha em uma lista, separada por vírgulas, e adiciona essa lista na lista `data`.
        data.append(line.split(','))
    
    # Calcula o total para cada mês
    # Cria uma lista chamada `totals` com o mesmo número de elementos que tem de colunas no CSV, com exceção da primeira coluna que tem os tipos de exames
    # Inicializa todos os valores dessa lista com zero, que vai ser usado pra armazenar o total de exames por mês
    totals = [0] * (len(headers) - 1)  # Exclua o primeiro campo de cabeçalho
```

```Python

    for row in data:
        try:
            # Ignorar a linha 'Total ' para não incluir nos cálculos
            # Verifica se o primeiro elemento da linha (que contém o nome do exame) é a string 'Total'. 
            # Se for, essa linha é ignorada, porque contém os totais finais, e não deve ser usada no cálculo
            if row[0].strip() == 'Total ':
                continue # Continua para a próxima iteração, ignorando a linha atual

            # Percorre as colunas a partir da segunda (índice 1), porque a primeira coluna está com os nomes dos exames e não os números    
            for i in range(1, len(row)):

                # Remove os pontos dos números (usados como separador de milhar) e troca as vírgulas por pontos que é o padrão numérico
                # Converte o valor para float e soma o valor na lista `totals` correspondente ao mês
                totals[i - 1] += float(row[i].replace('.', '').replace(',', '.'))

        # Se ocorrer um erro de conversão (por exemplo, se um valor não for um número), imprime a mensagem de erro.
        except ValueError:
            print(f"Erro ao processar a linha: {row}")

    # Printa a lista `totals`, que contém os totais de exames para cada mês
    print(f"Total de exames: {totals}")
    
    # Calcula o número de linhas de dados (excluindo a linha 'Total ' que foi ignorada)
    num_rows = len(data) - 1  # Exclua a linha 'Total'

    # Se tiver linhas de dados, calcula a média de exames para cada mês, dividindo o total de exames de cada mês pelo número de linhas
    if num_rows > 0:
        averages = [total / num_rows for total in totals]

    # E se não tiver linhas de dados (num_rows == 0), inicializa todas as médias como zero
    else:
        averages = [0] * len(totals)

    # Printa as médias calculadas para cada mês, formatadas com duas casas decimais
    print(f"Média de exames em janeiro: {averages[0]:.2f}")
    print(f"Média de exames em fevereiro: {averages[1]:.2f}")
    print(f"Média de exames em março: {averages[2]:.2f}")
    print(f"Média de exames em abril: {averages[3]:.2f}")
```

```Python
bucket_name = 'desafio-compass' # Nome do bucket no S3
file_key = 'exames_laboratoriais-janeiro-abril2024.csv' # Nome do arquivo no bucket
results = execute_s3_select(bucket_name, file_key) # Executa a primeira função `execute_s3_select` para buscar os dados do arquivo CSV no S3 e armazena o resultado em `results`
print("Resultado da consulta SQL:") # Printa uma mensagem informando que a consulta SQL foi executada
print(results) # Printa os resultados brutos da consulta (conteúdo do CSV)
process_results(results) # Chama a segunda função `process_results` para processar os resultados da consulta, calcular os totais e médias, e exibir eles
```

## Abaixo o trecho em que estão as consultas que tive problemas em executa-las
```Python
SELECT 
    # Duas funções de agregação, uma calcula a média dos exames de janeiro e a outra calcula o valor máximo dos exames de fevereiro
    AVG(CAST("janeiro" AS DOUBLE)) AS media_janeiro,  
    MAX(CAST("fevereiro" AS DOUBLE)) AS max_fevereiro, 

    # Função Condicional, pra verificar se o número de exames em março é maior que 5000. Se for, retorna 'ALTO', se não, retorna 'BAIXO'
    IF(CAST("marco" AS DOUBLE) > 5000, 'ALTO', 'BAIXO') AS status_marco, 

    # Função de string, extrai os primeiros 5 caracteres da coluna laboratorio, que pode ser útil se eu quiser analisar só uma parte do nome
    SUBSTRING("laboratorio", 1, 5) AS prefixo_laboratorio,  

    # Função de data
    YEAR(CAST("data" AS TIMESTAMP)) AS ano_data 
FROM s3object 

# Dois operadores lógicos, 'AND' e comparação '>' filtra os dados retornando apenas os registros onde o valor de exames de janeiro é maior que 1000 e o valor de fevereiro é maior que 2000.
WHERE (CAST("janeiro" AS DOUBLE) > 1000 AND CAST("fevereiro" AS DOUBLE) > 2000)  -- Dois operadores lógicos
GROUP BY "laboratorio", "data" 
```