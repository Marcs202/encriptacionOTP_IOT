

def scrambled(P, S):
    return ((P << (S & 0b11111)) | (P >> (64 - (S & 0b11111)))) & 0xFFFFFFFFFFFFFFFF
#(S & 0b11111) obtiene los bit menos significativos
def generative(P0, Q):
    return (P0 & Q) & 0xFFFFFFFFFFFFFFFF
#solo se usa un and y se corta a 64 bits
def mutative(S, Q):
    return (S | Q) & 0xFFFFFFFFFFFFFFFF
#or bit a bit 
def generate_keys(p, q, s, n):
    keys = []
    s0 = s
    for i in range(1,n+1):
        if i % 2 == 0:
            q0 = scrambled(q, s0)
            k = generative(q0, p0) # k = generative(q0, p0)
            s0 = mutative(s0, p0)  #  s0 = mutative(s0, p0)
        else: #!la primera iteracion empieza aca, ya que el for fue configurado para empezar en 1
            p0 = scrambled(p, s)
            k = generative(p0, q)
            s0 = mutative(s, q)
        keys.append(k)
        p, q = q, p0  # Swap p and q for the next iteration
    return keys
#la  funcion solo sigue los pasos del algorito que planteo en el 
#diagrama de flujo del paper 

p = 9223372036854775783
q = 9223372036854775643
s = 9223372036854775537
n = 10  # Number of iterations

#* Generate the keys
keys = generate_keys(p, q, s, 50)

for i, key in enumerate(keys):
    print(f"Key {i+1}: {key}")

#####! Definicion de funciones reversibles 
##? Funcion 1, XOR
 ##?para todas las funciones f1,f2,f3,f4, se capturara el mensaje
 ##? y se va a convertir las letras en codigo ASCII para que al array resultante se
 ##? se le apliquen las funciones reversibles
def fn1(message, key):
    mensaje_encriptado = [m ^ key for m in message] # el operador ^ es el XOR 
    return mensaje_encriptado

def fn1D(encrypted_message, key):
    mensaje_desencriptado = [em ^ key for em in encrypted_message]
    mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado) 
    ##al desencriptar el mensaje regresa el codigo ACII a letras
    return mensaje_desencriptado    

mensaje = input("Ingrese el mensaje a encriptar: \n \t--> ")
mensaje = [ord(c) for c in mensaje]

mensaje_encriptado = fn1(mensaje,keys[1])
print("Mensaje encriptado: ", mensaje_encriptado)
mensaje_desencriptado = fn1D(mensaje_encriptado,keys[1])
print ("Mensaje desencriptado: ", mensaje_desencriptado)


####? Funcion 2, Rotacion de bits
def left_rotate(n, d):
    return (n << (d % 64)) | (n >> (64 - (d % 64)))
# << rota a la izquierda, rota >> a la derecha
def right_rotate(n, d):
    return (n >> (d % 64)) | ((n << (64 - (d % 64))) & 0xFFFFFFFFFFFFFFFF)

def fn2(mensaje, key):
    mensajeA = [ord(c) for c in mensaje]
    mensaje_encriptado = [left_rotate(m, key % 64) for m in mensajeA]
    return mensaje_encriptado

def fn2D(encrypted_message, key):
    mensaje_desencriptado = [right_rotate(em, key % 64) for em in encrypted_message]
    mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
    return mensaje_desencriptado  

####? Funcion 3, suma y resta
mensaje = input("Ingrese el mensaje a encriptar: \n \t--> ")
mensaje_encriptado = fn2(mensaje,keys[1])
print("Mensaje encriptado: ", mensaje_encriptado)
mensaje_desencriptado = fn2D(mensaje_encriptado,keys[1])
print ("Mensaje desencriptado: ", mensaje_desencriptado)

##suma la llave a cada ASCII 
def suma2n(n, d):
    return (n + d) & 0xFFFFFFFFFFFFFFFF
##resta la llave a cada ASCII 
def resta2n(n, d):
    return (n - d) & 0xFFFFFFFFFFFFFFFF

def fn3(mensaje, key):
    mensajeA = [ord(c) for c in mensaje]
    mensaje_encriptado = [suma2n(m, key) for m in mensajeA]
    return mensaje_encriptado

def fn3D(encrypted_message, key):
    mensaje_desencriptado = [resta2n(em, key) for em in encrypted_message]
    mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
    return mensaje_desencriptado  

mensaje = input("Ingrese el mensaje a encriptar: \n \t--> ")
mensaje_encriptado = fn3(mensaje,keys[1])
print("Mensaje encriptado: ", mensaje_encriptado)
mensaje_desencriptado = fn3D(mensaje_encriptado,keys[1])
print ("Mensaje desencriptado: ", mensaje_desencriptado)


####? Funcion 4, inversion de bits, los 0 se hacen 1 y los 1 0

'''La operación XOR con una clave dada cambia algunos bits del mensaje original, 
dependiendo de los bits de la clave. Específicamente, un bit del mensaje se cambia 
si el bit correspondiente en la clave es 1, y se mantiene igual si el bit correspondiente 
en la clave es 0.
La inversión de bits, por otro lado, cambia todos los bits del mensaje, 
independientemente de la clave. Cada bit 0 se convierte en 1, y cada bit 1 se convierte en 0.'''
def bit_inversion(n):
    # Esta es una función de inversión de bits que invierte todos los bits de n
    return n ^ 0xFFFFFFFFFFFFFFFF

def fn4(mensaje, key):
    mensajeA = [ord(c) for c in mensaje]
    mensaje_encriptado= [bit_inversion(m ^ key) for m in mensajeA]
    return mensaje_encriptado
 

def fn4D(encrypted_message, key):
    mensaje_desencriptado = [bit_inversion(em) ^ key for em in encrypted_message]
    mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
    return mensaje_desencriptado


mensaje = input("Ingrese el mensaje a encriptar: \n \t--> ")
mensaje_encriptado = fn4(mensaje,keys[1])
print("Mensaje encriptado: ", mensaje_encriptado)
mensaje_desencriptado = fn4D(mensaje_encriptado,keys[1])
print ("Mensaje desencriptado: ", mensaje_desencriptado)