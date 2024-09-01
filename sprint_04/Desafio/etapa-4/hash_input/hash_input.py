import hashlib

while True:
    user_input = input("Digite uma string para gerar o hash ou 'sair' para encerrar: ")
    if user_input.lower() == 'sair':
        break
    
    hash_object = hashlib.sha1(user_input.encode())
    hash_hex = hash_object.hexdigest()
    
    print(f'O hash SHA-1 da string é: {hash_hex}')

