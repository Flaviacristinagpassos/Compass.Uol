## Na Sprint 2 pudemos aprender e trabalhar com SGBD

# Conceitos de Data Analytics I

**Diferença entre papeis envolvidos em Big Data**
- Cientista de Dados 
- Arquiteto de Soluções para Dados
- Engenheiro de Dados
- Desenvolvedores

**Tipos de Dados**
    - Literal
    - Dados Digitais
    - Informação
    - Conhecimento e Inteligência

**Classificação de Dados**
    - Estruturados (Banco de dados)
    - Semiestrutrados (XML, JSON, RDF, OWL)
    - Não-Estruturados (Textos, arquivos, documentos, imagens, v´deos...)

1. **Banco de Dados**
    - Banco de Dados Relacionais (Modelagem-estruturar os objetos antes de inseriri os dados)
    Tabelas, Colunas, Tuplas, Chaves
    2 possíveis arquiteturas OLAP (otimizado p/ realização de seleção e extração de dados, ideal p/ sistemas como de Data Warehouse-DW) e OLTP (otimizado p/ registrar transações, ideal p/ sistemas com interações com clientes ou sistemas transacionais)
    - Banco de Dados Não-Relacionais (NoSQL)
    Chave-valor, Orientado a Docuemntos, Orientado a Colunas, Orientado a Grafos

2. **Tipos de armazenamento de dados**
    - TXT, CSV, XML, JSON, ORC, PARQUET e AVRO.

3. **Data Lake (Arquitetura Lambda)**
    - Flexível
    - Nada haver com AWS, é um modelo de arquitetura BigData, é um modelo teórico
    - É dividida em três camadas: Batch layer, Speed layer e Serving layer


# Conceitos de Data Analytics II

## Técnicas para processamento de Dados(Batch e Stream)
- O Batch é um processamento em lote, é o processamento de diversas transações que ocorreram num sistema de origem e serão processadas para outros sistemas em conjunto ou em bloco. O Hadoop MapReduce é um dos melhores frameworks para processar dados em lotes.
- O stream é um processamento que trabalha com fluxos de dados que são capturados em tempo real e processados com latência mínima para o sistema de destino. Neste processamento uma ou um pequeno conjunto de transações é processada e enviada ao sistema de destino.

1. **Business Intelligence (BI)**
    - Inteligência de negócios, é um conjunto de teorias, metodologias, práticas, processos, tecnologias e estruturas para desenvolver uma inteligência ao negócio.
    - As principais funções de um BI são: relatórios, análises, mineração de dados, processamento de eventos complexos, gerenciamento de desempenho dos negócios, benchmarking, mineração de dados, análises previsíveis e análises prescritivas.

2. **Data Warehouse (DW)**
    - Armazém de Dados, tem por objetivo a centralização dos dados retirados de diversas origens para facilitar ou simplificar o consumo futuro.
    - É um repositório centralizado otimizado para análises.
    Enquanto um banco de dados transacional (OLTP) utiliza normalização de formato de dados, um DW utiliza dados em formado de-normalizados para aumentar o desempenho das consultas e torna-se mais
intuitivo para os utilizadores.

3. **Mineração de Dados**
    - É o processo de descobrir correlações, padrões e tendências significativos analisando grandes quantidades de dados armazenados em repositórios.

4. **Machine Learning**
    - O aprendizado de máquina é uma espécie de inteligência artificial que é responsável por fornecer aos computadores a capacidade de aprender sobre novos conjuntos de dados sem serem programados por meio de uma fonte explícita.
    - São algoritmos avançados de aprendizado de máquina compostos de muitas tecnologias (como deep learning, redes neurais e processamento de linguagem natural), usadas em aprendizado supervisionado e não supervisionado, que operam guiados por lições de informações existentes.

5. **Deep Learning**
    - É um tipo de machine learning com o objetivo de treinar computadores para realizar tarefas como seres humanos, o que inclui reconhecimento de fala, identificação de imagem e previsões.

6. **Relatórios**
    - É um documento que apresenta informações em um formato organizado para um público específico e propósito.

7. **Dashboards**
    - Basicamente é um indicador de negócios, pode ser um número ou um gráfico, um conjunto de dashboards chama-se painel de dados.
    - São personalizáveis para atender às necessidades específicas de um departamento e empresa. 
    - Por trás da dashboard, um painel se conecta a seus arquivos, anexos, serviços e APIs, exibindo todos esses dados na forma de tabelas, gráficos de linhas, gráficos de barras, indicadores, entre outras formas de visualização.

8. **Internet das coisas (IoT)**
    - São dispositivos físicos (veículos, videogames, edifícios, câmeras, sensores e outros dotados de tecnologia embarcada conexão com a rede) capaz de coletar e transmitir dados.

9. **API**
    - Especifica como os componentes de software devem interagir.
    - São usadas ao programar componentes da interface gráfica do usuário (GUI).
    - Compostas de dois elementos. 
    O primeiro é uma especificação que descreve como as informações são trocadas entre os programas, realizadas através de um request/solicitação de processamento e retornando os dados solicitados. 
    O segundo é uma interface de software escrita para que essa especificação esteja publicada de alguma forma para que o uso ocorra da forma correta. 
    - Existem 3 tipos básicos de APIs:
    Local: São a forma de comunicação básica. Geralmente são serviços de sistema operacional (SO) ou de middleware para programas (Java Database Connectivity-JDBC).
    Web-like: APIs da Web são projetadas para representar recursos amplamente usados, como páginas HTML, e são acessadas usando um protocolo HTTP simples. Qualquer URL da web ativa uma API da web. São geralmente chamadas de REST (representational state transfer) ou RESTful ou SOAP.
    Program-like: APIs de programa são baseadas na tecnologia de chamada de Remote Procedure Call (RPC) que faz com que um componente de programa remoto pareça ser local para o restante do software. (APIs de arquitetura orientada a serviços- SOA).

10. **Métodos de acesso à Banco de Dados**
    - Pela confusão causada pela proliferação de APIs nativas de acesso às bases de dados proprietárias, surgiu a ideia de uma API de acesso universal às bases de dados.
    A comunidade da área de bancos de dados formou um consórcio, chamado SAG (Standard Query Language Access Group) constituído por vários fornecedores, para prover um padrão unificado de linguagem para acesso à base de dados remotas. Assim, nasceu SQL CLI, definido pela SAG.
    - Uma CLI não é uma nova linguagem de consulta, é, simplesmente, uma interface procedural para SQL. As aplicações usam CLI para submeter statements SQL para um sistema gerenciador de base de dados (DBMS).
    - Uma CLI requer um driver para cada base de dados para qual ela se conecta. Cada driver deve ser escrito para uma tecnologia específica, usando os métodos de acesso existentes para bases de dados. A CLI provê um driver manager que fala com um driver através de uma SPI (Service Provider Interface).


# Modelagem de Dados
## Modelagem Relacional
- Uma idéia de que não é relevante ao usuário saber onde os dados estão ou como se encontram, é representada por uma coleção de tabelas, um conjunto de tuplas.

## Modelagem Dimensional
- O modo é favorecer o consumo por meio de ferramentas analíticas, OLAP, Online Analytical Processing. É a capacidade para manipular e analisar um grande volume de dados sob múltiplas perpectivas -cubos.

# AWS Builder
## AWS Partner
- Nesta 'builder' da amazon pudemos ter acesso ao curso de 'Sales Accreditation (Business)', onde estudamos sobre os seguintes tópicos:

1. **Conceitos de nuvem e serviços da AWS**
    - Computação em nuvem
    - Por que os clientes escolhem a AWS
    - Introdução aos serviços da AWS
    - Facilitando a transformação digital

2. **Valor comercial**
    - Valor comercial e testes comparativos
    - AWS Cloud Value Framework: Economia de custos, produtividade da equipe, resiliência operacional e agilidade empresarial

3. **Como lidar com objeções à nuvem**
    - Objeções à nuvem
    - Custo
    - Segurança, conformidade e privacidade
    - Perda de controle ou visibilidade
    - Infraestrutura atual
    - Déficit de habilidades
    - Atrelamento a fornecedor
    - Sustentabilidade

4. **Venda conjunta com a AWS**
    - Noções básicas da venda conjunta
    - Trabalhar com a AWS
    - Práticas recomendadas
    - Programas de financiamento para AWS Partners
