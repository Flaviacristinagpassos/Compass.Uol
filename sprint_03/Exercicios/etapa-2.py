import os

# Diretório onde o arquivo actors.csv está localizado
diretorio = '/home/nave/Área de Trabalho/exercicio'

# Caminho para o arquivo actors.csv
csv_path = os.path.join(diretorio, 'actors.csv')

# Leitura do arquivo linha por linha
with open(csv_path, 'r') as file:
    linhas = file.readlines()

# Inicializando variáveis para calcular a média
soma_gross = 0.0
contador = 0

# Iterar sobre as linhas do arquivo (exceto a primeira, que é o cabeçalho)
for linha in linhas[1:]:
    # Remover aspas para evitar problemas de separação
    linha = linha.replace('"', '')
    
    # Separar os campos por vírgula
    campos = linha.strip().split(',')
    
    # Verificar se a linha tem o número correto de colunas
    if len(campos) >= 6:
        try:
            # Extrair a receita bruta do principal filme (última coluna)
            gross = float(campos[5].strip())  # Gross está na última coluna (índice 5)
            soma_gross += gross
            contador += 1
        except ValueError:
            print(f"Erro ao converter a receita bruta. Valor encontrado: {campos[5]}")

# Calcular a média, se houver pelo menos um ator
if contador > 0:
    media_gross = soma_gross / contador
else:
    media_gross = 0.0

# Resultado a ser escrito no arquivo etapa-2.txt
resultado = f"Média de receita bruta dos principais filmes: {media_gross:.2f} milhões de dólares"

# Escrever o resultado no arquivo etapa-2.txt
with open(os.path.join(diretorio, 'etapa-2.txt'), 'w') as f:
    f.write(resultado)

print("Resultado:", resultado)
