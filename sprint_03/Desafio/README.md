# Desafio de Análise de Dados e Visualização

O objetivo deste desafio foi realizar uma análise detalhada dos dados de aplicativos usando o dataset googleplaystore.csv. A análise envolveu a criação de diversos gráficos para visualizar e entender melhor os dados. Os gráficos gerados foram:


1. **Gráfico de Linha: Média das Avaliações por Categoria**

2. **Gráfico de Barras Horizontais: Top 10 Aplicativos por Número de Avaliações com Número de Instalações Anotado**

3. **Gráfico de Dispersão: Relação entre Número de Instalações e Número de Avaliações**

4. **Gráfico de Área: Média de Avaliações por Número de Instalações**

5. **Gráfico de Barras: Top 10 Categorias com Mais Aplicativos**

6. **Gráfico de Linhas: Top 10 Categorias com Mais Aplicativos**

7. **Histograma: Contagens das Top 10 Categorias de Aplicativos**

## Requisitos
- Python 3.x
- Bibliotecas: matplotlib, pandas
- Dataset: googleplaystore.csv

## Passos Realizados
1. **Leitura e Limpeza dos Dados**

- O dataset foi carregado e as colunas necessárias foram limpas e convertidas para formatos apropriados.

2. **Análise e Visualização**

- Gráfico de Linha: Calculada a média das avaliações por categoria e visualizada em um gráfico de linha.
- Gráfico de Barras Horizontais: Selecionados os 10 aplicativos com mais instalações e visualizados com número de avaliações anotado.
- Gráfico de Dispersão: Relacionado o número de instalações com o número de avaliações em um gráfico de dispersão.
- Gráfico de Área: Calculada a média de avaliações por número de instalações e visualizada em um gráfico de área.
- Gráfico de Barras: Exibidas as 10 categorias com mais aplicativos.
- Gráfico de Linhas: Mostradas as 10 categorias com mais aplicativos em um gráfico de linhas.
- Histograma: Mostradas as contagens das 10 categorias de aplicativos mais populares.

# Código

Abaixo estão os códigos usados para gerar os gráficos:

1. **Gráfico de Linha: Média das Avaliações por Categoria**

```python 
    import matplotlib.pyplot as plt
    # Calcular a média das avaliações por categoria
    avg_ratings_by_category = df.groupby('Category')['Rating'].mean().sort_values()

    # Criar gráfico de linha
    plt.figure(figsize=(12, 6))
    plt.plot(avg_ratings_by_category.index, avg_ratings_by_category.values, marker='o', linestyle='-', color='b')
    plt.title('Média das Avaliações por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('media_avaliacoes_por_categoria.png')
    plt.show()
```

2. **Gráfico de Barras Horizontais: Número de Avaliações com Número de Instalações Anotado**

```python
import matplotlib.pyplot as plt

# Limpar e converter as colunas 'Installs' e 'Reviews'
df_cleaned['Installs'] = df_cleaned['Installs'].replace(r'[,\+]', '', regex=True).astype(float)
df_cleaned['Reviews'] = df_cleaned['Reviews'].astype(float)

# Selecionar os 10 aplicativos com mais instalações
top_10_installs_reviews = df_cleaned[['App', 'Installs', 'Reviews']].sort_values(by='Installs', ascending=False).head(10)

# Criar o gráfico de barras horizontais para Número de Avaliações
plt.figure(figsize=(14, 8))
bars = plt.barh(top_10_installs_reviews['App'], top_10_installs_reviews['Reviews'], color='teal')

# Adicionar números de Instalações como anotação nas barras
for bar, installs in zip(bars, top_10_installs_reviews['Installs']):
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{int(installs):,}', 
             va='center', ha='left', color='black', fontsize=10)

plt.title('Top 10 Aplicativos por Número de Avaliações com Número de Instalações Anotado')
plt.xlabel('Número de Avaliações')
plt.ylabel('Aplicativo')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('top_10_avaliacoes_com_instalacoes.png')
plt.show()
```

3. **Gráfico de Dispersão: Relação entre Número de Instalações e Número de Avaliações**

```python
import matplotlib.pyplot as plt

# Limpar e converter as colunas 'Installs' e 'Reviews'
df_cleaned['Installs'] = df_cleaned['Installs'].replace(r'[,\+]', '', regex=True).astype(float)
df_cleaned['Reviews'] = df_cleaned['Reviews'].astype(float)

# Criar o gráfico de dispersão
plt.figure(figsize=(10, 6))
plt.scatter(df_cleaned['Installs'], df_cleaned['Reviews'], alpha=0.5, edgecolors='w', s=50)
plt.title('Relação entre Número de Instalações e Número de Avaliações')
plt.xlabel('Número de Instalações')
plt.ylabel('Número de Avaliações')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('relacao_instalacoes_avaliacoes.png')
plt.show()
```

4. **Gráfico de Área: Média de Avaliações por Número de Instalações**

```python
import matplotlib.pyplot as plt

# Limpar e converter a coluna 'Installs'
df_cleaned['Installs'] = df_cleaned['Installs'].replace(r'[,\+]', '', regex=True).astype(float)

# Limpar e converter a coluna 'Reviews'
df_cleaned['Reviews'] = df_cleaned['Reviews'].astype(float)

# Calcular a média de avaliações por número de instalações
avg_reviews_by_installs = df_cleaned.groupby('Installs')['Reviews'].mean()

# Criar o gráfico de área
plt.figure(figsize=(12, 8))
plt.fill_between(avg_reviews_by_installs.index, avg_reviews_by_installs.values, color='skyblue', alpha=0.5)
plt.plot(avg_reviews_by_installs.index, avg_reviews_by_installs.values, color='blue', marker='o')
plt.title('Média de Avaliações por Número de Instalações')
plt.xlabel('Número de Instalações')
plt.ylabel('Média de Avaliações')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('media_avaliacoes_por_instalacoes.png')
plt.show()
```

5. **Gráfico de Barras: Top 10 Categorias com Mais Aplicativos**

```python
import matplotlib.pyplot as plt
import pandas as pd

# Calcular o número de aplicativos por categoria
category_counts = df['Category'].value_counts()

# Selecionar as 10 categorias com mais aplicativos
top_10_categories = category_counts.head(10)

# Criar o gráfico de barras
plt.figure(figsize=(12, 6))
top_10_categories.plot(kind='bar', color='skyblue')
plt.title('Top 10 Categorias com Mais Aplicativos')
plt.xlabel('Categoria')
plt.ylabel('Número de Aplicativos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_categorias_barras.png')
plt.show()
```

6. **Gráfico de Linhas: Top 10 Categorias com Mais Aplicativos**

```python
import matplotlib.pyplot as plt

# Calcular o número de aplicativos por categoria
category_counts = df['Category'].value_counts()

# Selecionar as 10 categorias com mais aplicativos
top_10_categories = category_counts.head(10)

# Criar o gráfico de linhas
plt.figure(figsize=(12, 6))
top_10_categories.plot(kind='line', marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.title('Top 10 Categorias com Mais Aplicativos')
plt.xlabel('Categoria')
plt.ylabel('Número de Aplicativos')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('top_10_categorias_linhas.png')
plt.show()
```

7. **Histograma: Contagens das Top 10 Categorias de Aplicativos**

```python
import matplotlib.pyplot as plt

# Calcular o número de aplicativos por categoria
category_counts = df['Category'].value_counts()

# Selecionar as 10 categorias com mais aplicativos
top_10_categories = category_counts.head(10)

# Criar o histograma
plt.figure(figsize=(12, 6))
plt.hist(top_10_categories, bins=len(top_10_categories), color='lightcoral', edgecolor='black', rwidth=0.8)
plt.title('Histograma das Contagens das Top 10 Categorias de Aplicativos')
plt.xlabel('Número de Aplicativos')
plt.ylabel('Número de Categorias')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('histograma_top_10_categorias.png')
plt.show()
```

# Resultados
Os gráficos gerados forneceram uma visão detalhada sobre:
- A distribuição das avaliações por categoria de aplicativos;
- A relação entre o número de avaliações e o número de instalações dos aplicativos;
- A média das avaliações em função do número de instalações;
- As categorias de aplicativos com mais aplicativos;
- A visualização das contagens das top 10 categorias;
- Os gráficos foram salvos como arquivos PNG para fácil visualização e análise.

# Conclusão
A análise e visualização dos dados fornecem uma visão abrangente sobre as características e a distribuição dos aplicativos no dataset. 

Esses insights podem ser úteis para tomar decisões mais informadas sobre tendências e padrões no mercado de aplicativos.




