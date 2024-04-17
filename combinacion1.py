p = 9223372036854775783
q = 9223372036854775643
s = 9223372036854775537
n = 50  # Number de llaves
#combinacion 1 de funciones f1,f2,f3,f4
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
def fn1(mensaje, key):
    mensaje_encriptado = [m ^ key for m in mensaje] # el operador ^ es el XOR 
    return mensaje_encriptado
def fn1D(encrypted_message, key):
    mensaje_desencriptado = [em ^ key for em in encrypted_message]
    ##al desencriptar el mensaje regresa el codigo ACII a letras
    return mensaje_desencriptado    
def left_rotate(n, d):
    return (n << (d % 64)) | (n >> (64 - (d % 64)))
# << rota a la izquierda, rota >> a la derecha
def right_rotate(n, d):
    return (n >> (d % 64)) | ((n << (64 - (d % 64))) & 0xFFFFFFFFFFFFFFFF)
def fn2(mensaje, key):
    mensaje_encriptado = [left_rotate(m, key % 64) for m in mensaje]
    return mensaje_encriptado
def fn2D(encrypted_message, key):
    mensaje_desencriptado = [right_rotate(em, key % 64) for em in encrypted_message]
    return mensaje_desencriptado
##suma la llave a cada ASCII 
def suma2n(n, d):
    return (n + d) & 0xFFFFFFFFFFFFFFFF
##resta la llave a cada ASCII 
def resta2n(n, d):
    return (n - d) & 0xFFFFFFFFFFFFFFFF
def fn3(mensaje, key):
    mensaje_encriptado = [suma2n(m, key) for m in mensaje]
    return mensaje_encriptado
def fn3D(encrypted_message, key):
    mensaje_desencriptado = [resta2n(em, key) for em in encrypted_message]
    return mensaje_desencriptado 
def bit_inversion(n):
    # Esta es una función de inversión de bits que invierte todos los bits de n
     return n ^ 0xFFFFFFFFFFFFFFFF
def fn4(mensaje, key):
    mensaje_encriptado= [bit_inversion(m ^ key) for m in mensaje]
    return mensaje_encriptado
def fn4D(encrypted_message, key):
    mensaje_desencriptado = [bit_inversion(em) ^ key for em in encrypted_message]
    return mensaje_desencriptado

keys = generate_keys(p, q, s, 50) #generar la llave 
mensaje = input("Ingrese el mensaje a cifrar:\n\t --> ") #Capturar el mensaje 
psn = '0000' #designando el PSN para probar nada mas 
mensajeASCII = [ord(c) for c in mensaje] #convierte en ACII el mensaje capturado
mensaje_desencriptado=""
if psn == '0000' or psn == '1111' or psn == '1110' or psn == '0001':
    #ejecutar f1->f2->f3->f4
    print(f"Los bits menos significativos del string son: {psn}")
    encriptadoF1 = fn1(mensajeASCII,keys[0]) 
    #devuelve el mensaje en un array con el size del string de cantidad de caracteres
    #por lo tanto ya no es necesario volver a utilizar la funcion ord
    encriptadoF2 =fn2(encriptadoF1,keys[0])
    encriptadoF3 = fn3(encriptadoF2,keys[0])
    encriptadoF4 = fn4(encriptadoF3,keys[0])
    desencriptadoF4 = fn4D(encriptadoF4,keys[0])
    desencriptadoF3 = fn3D (desencriptadoF4,keys[0])
    desencriptadoF2 = fn2D (desencriptadoF3,keys[0])
    desencriptadoF1 = fn1D (desencriptadoF2,keys[0])
    mensaje_desencriptado = desencriptadoF1
mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
print (mensaje_desencriptado)
