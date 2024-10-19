import random 

random.seed(40)
lista_numeros = [random.randint(1,1000) for _ in range(250)]

lista_numeros.reverse()
print(lista_numeros)
