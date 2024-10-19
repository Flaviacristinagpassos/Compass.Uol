import random
import time
import os
import names

random.seed(40)
qtd_nomes_unicos = 3000
qtd_nomes_aleatorios = 10000000

aux = []
for i in range(qtd_nomes_unicos):
    aux.append(names.get_full_name())

print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios..")
dados = []
for i in range(qtd_nomes_aleatorios):
    dados.append(random.choice(aux))

with open("nomes_aleatorios.txt", "w") as file:
    for nome in dados:
        file.write(f"{nome}\n")

print("Arquivo 'nomes_aleatorios.txt' gerado com sucesso!")

