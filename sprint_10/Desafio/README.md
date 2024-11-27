# Visão Geral do Desafio

O desafio consistiu em criar um Data Lake para dados de filmes e séries, com as seguintes etapas:

1. **Ingestão Batch de Arquivos CSV:** Ingestão inicial dos dados brutos na camada Raw Zone do Data Lake.
2. **Ingestão de Dados via API:** Complementação dos dados com informações adicionais da API do TMDB, gravadas na camada Raw Zone em formato JSON.
3. **Processamento e Refinamento:** Transformação e estruturação dos dados nas camadas Trusted e Refined para facilitar o consumo.
4. **Consumo dos Dados:** Criação de um dashboard no AWS QuickSight para análise e visualização, utilizando o AWS Athena como fonte de dados.


# Estrutura Esperada do Data Lake

Os dados deveriam ser organizados nas seguintes camadas no bucket S3:

**Raw Zone:** Dados brutos, como recebidos de fontes externas.

**Trusted Zone:** Dados validados, com formatação e estrutura mínima garantida.

**Refined Zone:** Dados otimizados para consumo analítico, com tabelas dimensionais e fato.

## **Arquivos na Refined Zone:**

**DimFilmes:** Contém IDs e títulos dos filmes.

**DimGenero:** Contém IDs e gêneros de filmes.

**FatoFilme:** Relaciona filmes e gêneros, com métricas agregadas.


# Etapas Desenvolvidas
1. **Ingestão Batch de Arquivos CSV**
Os arquivos movies.csv e series.csv foram carregados na Raw Zone do S3 com sucesso.

2. **Ingestão de Dados via API**
Usamos a API do TMDB para complementar os dados da Raw Zone. A coleta foi feita com sucesso, gerando arquivos JSON e armazenando-os no S3.

3. **Processamento e Refinamento**
Nesta etapa, os dados das zonas Raw e Trusted foram processados e transformados para criar tabelas na camada Refined.

**Problemas encontrados:**
- Erro de escrita dos arquivos Parquet: Embora os arquivos tenham sido salvos no S3, os registros não foram gravados corretamente, resultando em arquivos vazios.

**Impacto:**
 - As tabelas no Athena não tinham registros para consulta, bloqueando as etapas seguintes.


## 4. **Consumo dos Dados**

O objetivo era criar um dashboard no AWS QuickSight, utilizando o Athena como fonte de dados, para extrair insights analíticos.

**Problemas encontrados:**
- Como as tabelas do Athena estavam vazias, não foi possível configurar visualizações no QuickSight.

## **Causas dos Problemas:**

- Erro no Processamento: O código de processamento que converteu os dados para Parquet gerou arquivos sem registros.

**Causa:**
- Configurações incorretas no código Python.

**Falta de Validação:** 
Não houve uma validação adequada dos arquivos gerados antes de prosseguir para as etapas seguintes

**Permissões e Configurações:** 
Durante a integração do QuickSight com o Athena, ajustes de permissões no bucket S3 foram necessários, causando atrasos no processo

# Conclusão
Embora os dados tenham sido parcialmente processados e armazenados no S3, a etapa de refinamento apresentou falhas críticas que impossibilitaram a criação do dashboard final.
Isso destaca a importância de validar cada etapa do pipeline de dados e monitorar o estado dos arquivos gerados antes de prosseguir para etapas seguintes. O que me causou problemas na entrega final.

### Lições Aprendidas
**Validação:** 
Verificar os arquivos intermediários (como Parquet) para garantir que os dados estão corretos.

**Monitoramento de Logs:** 
Implementar logs detalhados para identificar e corrigir problemas mais rapidamente.

**Permissões:** 
Garantir que os papéis e políticas de acesso estão corretamente configurados desde o início.
