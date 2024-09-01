# Desafio de Python com Containers Dockers <img align="center" width=40 height=50 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" />

Este desafio consistiu em configurar e executar um ambiente utilizando Docker e Docker Compose. Abaixo estão descritos os passos realizados, os comandos utilizados e um resumo de como o ambiente foi configurado.

Adendo: Nesta mesma pasta 'Sesafio' em 'etapa-4', possui uma pasta chamada 'comandos.md', onde basicamente é o que está sendo explicado aqui porém de um jeito mais completo.

## Passos Realizados e Comandos Utilizados

## Criação do Arquivo Dockerfile
#### Comando:
```bash
gedit Dockerfile
```
#### Descrição: Utilizado o editor de texto gedit para criar e editar o Dockerfile. Esse arquivo foi utilizado para definir a imagem Docker personalizada, com instruções para configurar o ambiente dentro do container

## Construção da Imagem Docker
#### Comando:
```bash
docker build -t carguru-image .
```
#### Descrição: Construiu uma nova imagem Docker a partir do Dockerfile. A flag -t permite dar um nome à imagem, e o '.' indica que o Dockerfile está no diretório atual

## Executar container a partir da imagem
```bash
docker run --name carguru-container carguru-image
```

## Verificação dos Containers em Execução
#### Comando:
```bash
docker ps
```
#### Descrição: Exibiu a lista de containers em execução, permitindo verificar se todos os serviços foram inicializados corretamente

## Reiniciar o container parado
```bash
docker start carguru-container
```

## Construir a imagem Docker para o script
```bash
docker build -t mascarar-dados .
```

## Executar o container interativo para o script
```bash
docker run -it mascarar-dados
```

# Conclusão
Este desafio demonstrou como criar, configurar e executar containers utilizando Dockers. Através dos comandos e passos descritos, foi possível construir um ambiente isolado e funcional para a aplicação, facilitando o desenvolvimento e a implantação.

