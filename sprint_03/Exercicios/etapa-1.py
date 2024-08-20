import os

# Diretório onde o arquivo actors.csv está localizado
diretorio = '/home/nave/Área de Trabalho/exercicio'

# Caminho para o arquivo actors.csv
csv_path = os.path.join(diretorio, 'actors.csv')

# Leitura do arquivo linha por linha
with open(csv_path, 'r') as file:
    # Armazenar as linhas em uma lista
    linhas = file.readlines()

# Inicializando variáveis para armazenar o ator/atriz com maior número de filmes
maior_numero_filmes = 0
ator_maior_numero_filmes = ""

# Iterar sobre as linhas do arquivo (exceto a primeira, que é o cabeçalho)
for linha in linhas[1:]:
    linha = linha.replace('"', '')
    campos = linha.strip().split('\t')

    if len(campos) != 6:
        campos = linha.strip().split(',')  
    # Verificar o conteúdo lido
    print("Campos lidos:", campos)

    if len(campos) >= 3:
        ator = campos[0].strip()
        try:
                numero_filmes = int(campos[2].strip())  # Número de filmes está na 3ª coluna (índice 2)
        except ValueError:
            print(f"Erro ao converter o número de filmes para {ator}. Valor encontrado: {campos[2]}")
            continue  # Pular esta linha em caso de erro       
        # Comparar o número de filmes
        if numero_filmes > maior_numero_filmes:
            maior_numero_filmes = numero_filmes
            ator_maior_numero_filmes = ator

if ator_maior_numero_filmes:
# Resultado a ser escrito no arquivo etapa-1.txt
    resultado = f"Ator/Atriz com maior número de filmes: {ator_maior_numero_filmes}, Quantidade de filmes: {maior_numero_filmes}"
else:
    resultado = "Nenhum ator/atriz encontrado."

# Escrever o resultado no arquivo etapa-1.txt
with open(os.path.join(diretorio, 'etapa-1.txt'), 'w') as f:
    f.write(resultado)

print("Resultado:",resultado)
