## Na evidencia-2.png sobre a reutilização do Container

Ele verifica os Containers parados

Lista todos os containers, incluindo os parados, para verificar o status do container que foi criado com o comando: 
```bash
docker ps -a
```

ele mostra uma lista de containers. O container 'carguru-container' esta listado como parado 'Exited (0)'.


## Reiniciar um Container Parado

Como o container carguru-container esta parado, ele é reiniciado com o seguinte comando: 
```bash
docker start carguru-container
```

Para verificar se o container foi reiniciado corretamente e está em execução(Este comando listará apenas os containers em execução), foi executado o comando:
```bash
docker ps
```

