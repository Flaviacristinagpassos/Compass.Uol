import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('~/Downloads/nomes.csv')

# Criar uma nova coluna para a década
df['decada'] = (df['ano'] // 10) * 10

# Filtrar apenas as décadas a partir de 1950
df = df[df['decada'] >= 1950]

# Agrupar por década e nome, somando os totais
nomes_decada = df.groupby(['decada', 'nome']).agg({'total': 'sum'}).reset_index()

# Obter os três nomes mais comuns por década
top_3_por_decada = nomes_decada.groupby('decada').apply(lambda x: x.nlargest(3, 'total')).reset_index(drop=True)

# Exibir o resultado
print(top_3_por_decada)

# salvar o resultado em um arquivo CSV
top_3_por_decada.to_csv('top_3_por_decada.csv', index=False)

