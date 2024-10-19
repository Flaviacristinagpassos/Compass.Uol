animais = ["Cachorro", "Gato", "Coelho", "Coruja", "Rato", "Macaco", "Panda", "Cavalo", "Lobo", "Jacaré", "Bisão", "Gnus", "Leão", "Tigre", "Tucano", "Gambá", "Abelha", "Besouro", "Girafa", "Ovelha"]

animais_ordenados = sorted(animais)

[print(animal)for animal in animais_ordenados]

with open ("animais.csv", "w") as file:
	for animal in animais_ordenados:
		file.write(f"{animal}\n")
