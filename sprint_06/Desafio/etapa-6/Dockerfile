# Usar uma imagem base do Python
FROM python:3.8-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o código Python para o container
COPY . .

# Comando para rodar o script Python
CMD ["python", "ingestao.py"]

