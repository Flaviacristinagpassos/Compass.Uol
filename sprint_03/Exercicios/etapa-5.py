import os

# Diretório onde o arquivo actors.csv está localizado
diretorio = '/home/nave/Área de Trabalho/exercicio'

# Caminho para o arquivo actors.csv
csv_path = os.path.join(diretorio, 'actors.csv')

# Leitura do arquivo linha por linha
with open(csv_path, 'r') as file:
    linhas = file.readlines()

# Inicializando uma lista para armazenar os dados dos atores
atores = []

# Iterar sobre as linhas do arquivo (exceto a primeira, que é o cabeçalho)
for linha in linhas[1:]:
    # Remover aspas para evitar problemas de separação
    linha = linha.replace('"', '')
    
    # Separar os campos por vírgula
    campos = linha.strip().split(',')
    
    # Verificar se a linha tem o número correto de colunas
    if len(campos) >= 2:
        ator = campos[0].strip()  # Nome do ator está na 1ª coluna (índice 0)
        try:
            # Extrair a receita bruta total
            receita_bruta = float(campos[1].strip())  # Total Gross está na 2ª coluna (índice 1)
            atores.append((ator, receita_bruta))
        except ValueError:
            print(f"Erro ao converter a receita bruta total para {ator}. Valor encontrado: {campos[1]}")

# Ordenar os atores pela receita bruta total em ordem decrescente
atores_ordenados = sorted(atores, key=lambda x: -x[1])

# Escrever o resultado no arquivo etapa-5.txt
with open(os.path.join(diretorio, 'etapa-5.txt'), 'w') as f:
    for ator, receita_bruta in atores_ordenados:
        f.write(f"{ator} - {receita_bruta:.2f} milhões de dólares\n")

# Exibir o resultado no terminal (opcional)
for ator, receita_bruta in atores_ordenados:
    print(f"{ator} - {receita_bruta:.2f} milhões de dólares")
