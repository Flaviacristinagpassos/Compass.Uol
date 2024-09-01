# Etapa 1: Configuração Inicial e Dockerfile para carguru.py

## Criar o arquivo Dockerfile
```bash
gedit Dockerfile
```
## Adicionar o conteúdo do Dockerfile
```python
FROM python:3.9-slim

WORKDIR /desafio

COPY carguru.py .

CMD ["python", "carguru.py"]
```

## Construir a imagem Docker
```bash
docker build -t carguru-image .
```

## Executar o container a partir da imagem
```bash
docker run --name carguru-container carguru-image
```

# Etapa 2: 

## Verificar o status dos containers
```bash
docker ps -a
```

## Reiniciar o container parado
```bash
docker start carguru-container
```

# Etapa 3: Criação do Script 'hash_input.py' e 'Dockerfile'

## Criar o arquivo 'hash_input.py'
```bash
gedit hash_input.py
```

## Adicionar o conteúdo do script Python
```python
import hashlib

while True:
    user_input = input("Digite uma string para gerar o hash (ou 'sair' para encerrar): ")
    if user_input.lower() == 'sair':
        break

    # Gera o hash SHA-1 da string
    hash_object = hashlib.sha1(user_input.encode())

    # Converte o hash em uma string hexadecimal
    hash_hex = hash_object.hexdigest()

    print(f'O hash SHA-1 da string é: {hash_hex}')
```

## Criar o 'Dockerfile' para o script 'hash_input.py'
```bash
gedit Dockerfile
```

## Adicionar o conteúdo do Dockerfile
```python
FROM python:3.9-slim

WORKDIR /app

COPY hash_input.py .

CMD ["python", "hash_input.py"]
```

## Construir a imagem Docker para o script
```bash
docker build -t mascarar-dados .
```

## Executar o container interativo para o script
```bash
docker run -it mascarar-dados
```
