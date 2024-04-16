def reversible_encryption(message, key):
    encrypted_message = [m ^ key for m in message]
    return encrypted_message

def reversible_decryption(encrypted_message, key):
    decrypted_message = [em ^ key for em in encrypted_message]
    return decrypted_message

# Definir un mensaje y una clave
message = [ord(c) for c in "Hola Mundo"]
key = 9223372036854775783

print ("El mensaje sin cifrar es: ",message)
# Cifrar el mensaje
encrypted_message = reversible_encryption(message, key)
print("Mensaje cifrado:", encrypted_message)

# Descifrar el mensaje
decrypted_message = reversible_decryption(encrypted_message, key)
decrypted_message = ''.join(chr(i) for i in decrypted_message)
print("Mensaje descifrado:", decrypted_message)
