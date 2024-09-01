## Na evidencia-1.png temos o print do terminal sobre a execução do desafio.
Por questões de privacidade os arquivos na execução do ls estão cobertos.

No print ele esta construindo a imagem Docker, usando o Dockerfile que foi criando no comando 'gedit Dockerfile'

```bash
-t carguru-image # Define o nome da imagem como carguru-image
. # O ponto indica que o Docker deve procurar o Dockerfile no diretório atual (app)
```

## Executar o container
Após construir a imagem, e executar o container:

```bash
--name carguru-container # Dá um nome ao container que está sendo criado
carguru-image # Nome da imagem que foi contruído
```

O comando 'docker run' exibe a saída do script carguru.py.
A mensagem gerada pelo script será "Você deve dirigir um [carro aleatório]"