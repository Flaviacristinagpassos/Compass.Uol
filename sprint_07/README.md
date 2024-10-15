## Na Sprint 7 foi desenvolvido:

A parte 2 da entrega do desafio, ingestão po api, além de exercicios no laboratório Glue, leitura sobre o hadoop, também pude botar em prática o que foi aprendido no curso de spark no exercicio de contador de palavras com pyspark.

1. **No curso de Spark foram abordados os seguintes tópicos:**
    - DataFrames e RDDS
    - Spark SQL
    - Aplicações
    - Otimizações
    - Outros aspectos como:
        - Spark com notebook no Jupyter
        - Converter Pandas pra DataFrame do Spark
        - Spark UI

2. **Na entrega 2 do Desafio foi desenvolvido:**
    - Configuração da API 
        - Configuração do acesso à API do TMDB, incluindo o armazenamento seguro de credenciais em um arquivo .env.
    - Desenvolvimento do Script de Ingestão 
        - Criação de um script em Python (API-ingestao.py) responsável por realizar chamadas à API do TMDB e coletar dados de filmes e séries, agrupando as informações em arquivos JSON com um limite de 100 registros por arquivo.
    - Estruturação de Dados
        - Os dados foram organizados em diretórios específicos no Amazon S3, seguindo a estrutura de pastas definida para facilitar a consulta e a análise futura.
    - Consultas e Análises 
        - Realização de várias consultas no AWS Athena para validar e analisar os dados inseridos, incluindo contagens e médias, visando identificar a qualidade e a riqueza das informações
[Desafio] (./Desafio)

3. **Contador de Palavras com Apache Spark**
    - Instalação de dependências
    - Inicialização da sessão Spark
    - Leitura do arquivo de texto
    - Contagem de palavras
    - Encerramento da sessão Spark
[Exercicios] (./Exercicios)

4. **Lab Glue**
    - Construção de um processo de ETL simplificado utilizando o serviço AWS Glue
    - Preparar o dados de origem
    - Criar a IAM Role para os jobs do AWS Glue
    - Configurar as permissões no AWS Lake Formation
    - Criar novo job no AWS Glue
    - Criar novo Crawler

# Certificados
Também acabei vendo sobre ML e outros tópicos no curso completo de Spark e outro curso de preparatório também
[Certificados] (./Certificados)

# Evidências
E a execução de todos os passos estão na pasta evidencias
[Evidencias] (./Evidencias)


