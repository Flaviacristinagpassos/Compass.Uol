## <img align="center" width=40 height=60 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachespark/apachespark-original.svg" /> Análise de Dados com PySpark e Geração de Dados em Massa 

### Objetivo
**O objetivo do primeiro exercício sobre geração e massa de dados é demonstrar a geração de dados aleatórios utilizando Python. O projeto é dividido em três partes principais:**
- Geração de 250 números inteiros aleatórios
- Criação e ordenação de uma lista de animais
- Geração de um dataset contendo 10 milhões de nomes aleatórios

## 1. **Geração de Números Aleatórios**
```Python
import random 

random.seed(40) # Define a semente para a geração de números aleatórios
lista_numeros = [random.randint(1,1000) for _ in range(250)] # Gera 250 números aleatórios entre 1 e 1000

lista_numeros.reverse() # Inverte a ordem da lista
print(lista_numeros) # Printa a lista de números
```

## 2. **Criação e Ordenação de Animais**
```Python
animais = ["Cachorro", "Gato", "Coelho", "Coruja", "Rato", "Macaco", "Panda", "Cavalo", "Lobo", "Jacaré", "Bisão", "Gnus", "Leão", "Tigre", "Tucano", "Gambá", "Abelha", "Besouro", "Girafa", "Ovelha"]

animais_ordenados = sorted(animais)  # Ordena a lista de animais em ordem alfabética

[print(animal)for animal in animais_ordenados] # Imprime cada animal da lista ordenada

with open ("animais.csv", "w") as file: # Cria um arquivo CSV para armazenar os animais
	for animal in animais_ordenados: 
		file.write(f"{animal}\n") # Escreve cada animal em uma nova linha no arquivo
```

## 3. **Geração de Nomes Aleatórios**
```Python
import random
import time
import os
import names

random.seed(40) # Define a semente para garantir a geração de nomes aleatórios consistentes
qtd_nomes_unicos = 3000 # Número de nomes únicos a serem gerados
qtd_nomes_aleatorios = 10000000 # Total de nomes aleatórios a serem gerados

aux = [] # Inicializa uma lista vazia para armazenar os nomes ÙNICOS
for i in range(qtd_nomes_unicos): # itera x vezes,a cada iteração, chama names.get pra gerar um nome completo o adiciona na lista aux (aux.append)
    aux.append(names.get_full_name()) # Gera e adiciona nomes completos na lista 'aux'

print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios..")

dados = [] # Inicializa uma lista vazia para armazenar os nomes ALEATÒRIOS 
for i in range(qtd_nomes_aleatorios): # itera 10 milhões de vezes, pra cada iteração, seleciona de forma aleatória um nome da lista aux (random.choice(aux)) e adiciona na lista dados
    dados.append(random.choice(aux)) # Seleciona aleatoriamente nomes da lista 'aux'

with open("nomes_aleatorios.txt", "w") as file: # Cria um arquivo para armazenar os nomes aleatórios, vai abrir um arquivo chamado nomes_aleatorios.txt em modo de escrita (write)
    for nome in dados: # itera sobre cada nome na lista dados
        file.write(f"{nome}\n") # Pra cada iteração, escreve o nome em uma nova linha no arquivo

print("Arquivo 'nomes_aleatorios.txt' gerado com sucesso!")
```



### Objetivo
**O objetivo do segundo exercicio era de demonstrar o uso do Apache Spark para manipulação de dados, incluindo leitura de arquivos, transformação de dados e consultas SQL. O projeto é dividido em várias etapas, cada uma focada em um aspecto específico da manipulação de dados usando Spark**

## 1. **Criar SparkSession e Carregar o Arquivo**
```Python
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \ 
    .getOrCreate() # Cria a SparkSession ou obtém uma existente 

df_nomes = spark.read.csv("nomes_aleatorios.txt", header=False, inferSchema=True) # Lê um arquivo CSV sem cabeçalho e infere os tipos
df_nomes.show(5) # Mostra as 5 primeiras linhas do DataFrame
```

## 2. **Renomear Coluna e Imprimir Esquema**
```Python
df_nomes = df_nomes.withColumnRenamed("_c0", "Nome") # Renomeia a coluna padrão "_c0" pra "Nome"
df_nomes.printSchema() # Imprime o esquema do DataFrame, mostrando os nomes e tipos das colunas
df_nomes.show(10) # Mostra as 10 primeiras linhas do DataFrame
```

## 3. **Adicionar Coluna 'Escolaridade'**
```Python
df_nomes = df_nomes.withColumn( # Adiciona uma nova coluna ao DataFrame
    "Escolaridade", # Nome da nova coluna
    when(rand() < 0.33, "Fundamental") # Se um número aleatório for menor que 33%, atribui "Fundamental"
    .when((rand() >= 0.33) & (rand() < 0.66), "Medio") # Se estiver entre 0.33 e 0.66, atribui "Medio"
    .otherwise("Superior") # Caso contrário, atribui "Superior", 34%
)
df_nomes.show(10) # Mostra as 10 primeiras linhas do DataFrame com a nova coluna
```

## 4. **Adicionar Coluna 'País'**
```Python
paises = ["Argentina", "Brasil", "Chile", "Colômbia", "Equador", "Guiana", "Paraguai", "Peru", "Suriname", "Uruguai", "Venezuela", "Bolívia", "Guiana Francesa"]

# Função para selecionar país aleatório
@udf # Define uma função de usuário (UDF) pro uso no Spark
def pais_aleatorio(): # Define a função
    return choice(paises) # Retorna um país aleatório da lista

df_nomes = df_nomes.withColumn("Pais", pais_aleatorio()) # Adiciona a nova coluna "Pais" com países aleatórios
df_nomes.show(10) # Mostra as 10 primeiras linhas do DataFrame com a nova coluna
```

## 5. **Adicionar Coluna 'AnoNascimento'**
```Python
df_nomes = df_nomes.withColumn("AnoNascimento", (rand() * (2010 - 1945) + 1945).cast("int")) # Adiciona uma coluna "AnoNascimento" com anos aleatórios entre 1945 e 2010
df_nomes.show(10) # Mostra as 10 primeiras linhas do DataFrame com a nova coluna
```

## 6. **Selecionar Pessoas Nascidas no Século 21**
```Python
df_select = df_nomes.filter(df_nomes.AnoNascimento >= 2000) # Filtra o DataFrame para selecionar pessoas nascidas a partir de 2000
df_select.show(10) # Mostra as 10 primeiras linhas do DataFrame filtrado
```

## 7. **Usar Spark SQL para Selecionar Pessoas Nascidas no Século 21**
```Python
df_nomes.createOrReplaceTempView("pessoas") # Cria uma tabela temporária chamada "pessoas" para consultas SQL
spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000").show(10)  # Executa uma consulta SQL para selecionar pessoas nascidas a partir de 2000
``` 

## 8. **Contar Millennials**
```Python
millennials_count = df_nomes.filter((df_nomes.AnoNascimento >= 1980) & (df_nomes.AnoNascimento <= 1994)).count() # Conta o número de pessoas nascidas entre 1980 e 1994
print(f"Número de Millenials: {millennials_count}") # Printa o número de Millennials
```

## 9. **Contar Millennials Usando Spark SQL**
```Python
spark.sql("SELECT COUNT(*) FROM pessoas WHERE AnoNascimento BETWEEN 1980 AND 1994").show() # Executa uma consulta SQL para contar Millennials
```

## 10. **Contar Pessoas de Cada Geração por País**
```Python
geracoes_sql = """  # Define uma string com a consulta SQL pra contar pessoas por geração
SELECT Pais, 
       CASE
           WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
           WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geracao X'
           WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
           WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geracao Z'
       END AS Geracao, # Nomeia a coluna resultante como 'Geracao'
       COUNT(*) AS Quantidade # Conta o número de pessoas em cada geração
FROM pessoas # Especifica a tabela temporária
GROUP BY Pais, Geracao # Agrupa os resultados por país e geração
ORDER BY Pais, Geracao # Ordena os resultados por país e geração
"""

df_geracoes = spark.sql(geracoes_sql)  # Executa a consulta SQL e armazena os resultados em um DataFrame
df_geracoes.show() # Mostra os resultados da consulta
```

# Conclusão
O primeiro exercicio sobre geração e massa de dados demonstrou a capacidade de gerar dados aleatórios, criar e ordenar listas, e compor um dataset significativo utilizando Python. As técnicas utilizadas são essenciais para manipulação de dados e têm aplicações práticas em análise de dados, ciência de dados e desenvolvimento de software.

O segundo exercicio com o uso de ApacheSpark demonstrou como utilizar o Apache Spark para manipular e analisar dados de forma eficiente. Através das etapas descritas, foi possível carregar dados, adicionar colunas, realizar filtragens e executar consultas SQL, demonstrando a flexibilidade e poder do Apache Spark na análise de grandes volumes de dados.

# Certificados
Foi adquirido o certificado de Data&Analytics 8, e mias dois cursos pequenos de EAP e Gestão, em 
[Certificados](./Certificados)

# Evidências
E a execução das etapas dos exercicios estão na pasta evidencias, bem copo, as evidências do Desafio. Por conta dos arquivo nomes_aleatórios.txt ser muito grande, esta em formato de print nas evidências.
[Evidencias](./Evidencias)
