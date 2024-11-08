# Nesta Sprint foi feito a entrega 4 do Desafio.
# Estrutura do Projeto

O projeto segue uma arquitetura de Data Lake com 3 camadas principais:
    - Raw Zone (ou Raw Layer) – Dados brutos.
    - Trusted Zone (ou Trusted Layer) – Dados limpos e verificados.
    - Refined Zone (ou Refined Layer) – Dados preparados para análises avançadas.

Além disso, utiliza o AWS Glue para orquestrar o processo ETL (Extract, Transform, Load), Amazon S3 para armazenamento dos dados e PySpark para processamento em larga escala

# Estrutura de Pastas no S3
## O armazenamento dos dados é feito no Amazon S3. Cada camada é organizada em pastas separadas:

    - Raw Zone: s3://data-lake-flavia-passos/Raw/
    - Trusted Zone: s3://data-lake-flavia-passos/Trusted/
    - Refined Zone: s3://data-lake-flavia-passos/Refined/

## Funcionalidades Implementadas desde a Sprint 6

1. Ingestão de Dados
    - Os dados foram ingeridos de diferentes fontes:
    - Dados de filmes foram carregados do arquivo Movies em formato Parquet.
    - A ingestão de dados foi realizada utilizando o AWS Glue para ler e transformar os dados, processando-os na camada Trusted e gerando os arquivos necessários.

2. Criação das Tabelas no Refined
    - Tabelas de Fatos e Dimensões foram criadas com base nas necessidades analíticas do projeto:
    - FatoFilmes: Tabela de fatos que contém informações sobre filmes, agrupados por gênero (Drama e Romance).
    - DimFilme: Dimensão com detalhes sobre os filmes, como id_filme e titulo.
    - DimGenero: Dimensão com detalhes sobre os gêneros, como id_genero e genero.

3. Transformação dos Dados com PySpark
    - PySpark foi utilizado para realizar o processamento dos dados:
    - A tabela de fatos foi filtrada para considerar apenas filmes dos gêneros Drama e Romance.
    - A agregação foi realizada utilizando funções como countDistinct e count, para calcular o número de títulos e o total de filmes por gênero.

4. Armazenamento no S3
    - Os dados processados foram armazenados no Amazon S3 na camada Refined no formato Parquet, que oferece alta performance para leitura e escrita.

5. Orquestração com AWS Glue
    - O AWS Glue foi utilizado para orquestrar o processo de ETL, desde a ingestão dos dados até o armazenamento das tabelas de fatos e dimensões na camada Refined.
    - O job foi criado com o nome Refined_Processamento_Drama_Romance, responsável por:
        - Ler dados da Trusted Zone.
        - Processar e gerar as tabelas de fatos e dimensões.
        - Armazenar os resultados na camada Refined.

6. Processamento
    - Código na pasta 
    [Desafio](./Desafio/etapa-9/)


7. Camada Curated (Futura), Sprint 10
    - Depois da criação das camadas Refined, os dados poderão ser mais agregados e otimizados na camada Curated para análises e relatórios.


# Execução do Job
1. Configuração do AWS Glue Job
    - O job foi configurado no AWS Glue para realizar as seguintes operações:
    - Ler dados de filmes a partir da Trusted Zone.
    - Criar as tabelas FatoFilmes, DimFilme, e DimGenero.
    - Salvar os resultados na camada Refined.

2. Nome do Job
    - O job foi nomeado como Refined_Processamento_Drama_Romance, e configurado para rodar de forma automática no AWS Glue.


# Conclusão
Com o projeto implementado até o momento, todos os passos necessários para processar e armazenar os dados nas camadas Trusted e Refined foram completados durante o andamento das Sprints. A próxima etapa provavelmente possa envolver a criação da camada Curated, bem como a análise e visualização dos dados.

# Certificados
Foi adquirido o certificado de Data&Analytics 9, em 
[Certificados](./Certificados)

# Evidências
E a execução da etapa do Desafio esta na pasta evidencias.
[Evidencias](./Evidencias)