import os
from collections import Counter

# Diretório onde o arquivo actors.csv está localizado
diretorio = '/home/nave/Área de Trabalho/exercicio'

# Caminho para o arquivo actors.csv
csv_path = os.path.join(diretorio, 'actors.csv')

# Leitura do arquivo linha por linha
with open(csv_path, 'r') as file:
    linhas = file.readlines()

# Inicializando o contador para os filmes
contador_filmes = Counter()

# Iterar sobre as linhas do arquivo (exceto a primeira, que é o cabeçalho)
for linha in linhas[1:]:
    # Remover aspas para evitar problemas de separação
    linha = linha.replace('"', '')
    
    # Separar os campos por vírgula
    campos = linha.strip().split(',')
    
    # Verificar se a linha tem o número correto de colunas
    if len(campos) >= 5:
        # Extrair o nome do filme de maior bilheteira
        filme = campos[4].strip()  # #1 Movie está na 5ª coluna (índice 4)
        contador_filmes[filme] += 1

# Ordenar os filmes pela quantidade de aparições em ordem decrescente e, em caso de empate, pelo nome do filme
filmes_ordenados = sorted(contador_filmes.items(), key=lambda x: (-x[1], x[0]))

# Escrever o resultado no arquivo etapa-4.txt
with open(os.path.join(diretorio, 'etapa-4.txt'), 'w') as f:
    for filme, quantidade in filmes_ordenados:
        f.write(f"{filme} aparece {quantidade} vez(es) no dataset\n")

# Exibir o resultado no terminal (opcional)
for filme, quantidade in filmes_ordenados:
    print(f"{filme} aparece {quantidade} vez(es) no dataset")
