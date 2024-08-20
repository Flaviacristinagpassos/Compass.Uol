import os

# Diretório onde o arquivo actors.csv está localizado
diretorio = '/home/nave/Área de Trabalho/exercicio'

# Caminho para o arquivo actors.csv
csv_path = os.path.join(diretorio, 'actors.csv')

# Leitura do arquivo linha por linha
with open(csv_path, 'r') as file:
    linhas = file.readlines()

# Inicializando variáveis para encontrar o ator/atriz com a maior média de receita
maior_media = 0.0
ator_maior_media = ""

# Iterar sobre as linhas do arquivo (exceto a primeira, que é o cabeçalho)
for linha in linhas[1:]:
    # Remover aspas para evitar problemas de separação
    linha = linha.replace('"', '')
    
    # Separar os campos por vírgula
    campos = linha.strip().split(',')
    
    # Verificar se a linha tem o número correto de colunas
    if len(campos) >= 4:
        ator = campos[0].strip()
        try:
            # Extrair a média de receita por filme
            media_por_filme = float(campos[3].strip())  # Average per movie está na 4ª coluna (índice 3)
            
            # Comparar a média
            if media_por_filme > maior_media:
                maior_media = media_por_filme
                ator_maior_media = ator
        except ValueError:
            print(f"Erro ao converter a média de receita por filme para {ator}. Valor encontrado: {campos[3]}")

# Verificar se algum ator/atriz foi encontrado
if ator_maior_media:
    resultado = f"Ator/Atriz com a maior média de receita de bilheteira bruta por filme: {ator_maior_media}, Média por filme: {maior_media:.2f} milhões de dólares"
else:
    resultado = "Nenhum ator/atriz encontrado."

# Escrever o resultado no arquivo etapa-3.txt
with open(os.path.join(diretorio, 'etapa-3.txt'), 'w') as f:
    f.write(resultado)

print("Resultado:", resultado)
