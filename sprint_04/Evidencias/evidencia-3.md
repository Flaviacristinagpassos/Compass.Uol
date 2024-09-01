# Etapa-2

Vale ressaltar que preferi, dentro da pasta 'app' fazer uma pasta para 'carguru' com os arquivos 'carguru.py' e 'Dockerfile e uma para 'hash_input' com os arquivos 'hash_input.py' e 'Dockerfile'.

## Criar o Novo Script Python

Criei um arquivo chamado 'hash_input.py' com o código abaixo. Este script irá ler uma string do usuário, gerar o hash SHA-1, e exibir o resultado

```python
import hashlib

while True:
    # Recebe a string do usuário
    user_input = input("Digite uma string para gerar o hash (ou 'sair' para encerrar): ")
    if user_input.lower() == 'sair':
        break
    
    # Gera o hash SHA-1 da string
    hash_object = hashlib.sha1(user_input.encode())
    hash_hex = hash_object.hexdigest()
    
    # Exibe o hash
    print(f'O hash SHA-1 da string é: {hash_hex}')
```

## Construir a Nova Imagem Docker
Naveguei até o diretório onde estava meu arquivo 'hash_input.py' e 'Dockerfile', e construi a nova imagem Docker com o comando:

```bash
docker build -t mascarar-dados -f Dockerfile .  
```
```bash
-t mascarar-dados # Define o nome da imagem como 'mascarar-dados'
-f Dockerfile . # Especifica que deve usar o Dockerfile no diretório atual.
```

## Iniciar o Container a Partir da Nova Imagem
Foi executado um container a partir da imagem que tinha acabado de criar. Isso inicia o script 'hash_input.py' e permite que o usuário insira os dados:
```bash
docker run -it mascarar-dados
```
```bash
-it # Habilita a interação com o terminal do container
```

A string que testei foi 'u0L' com 'u' mínusculo, zero, e 'L' maíusculo