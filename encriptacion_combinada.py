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

class Encriptacion ():
    def combinacion1(mensaje,key):
        mensajeASCII = [ord(c) for c in mensaje]
        encriptadoF1 = fn1(mensajeASCII,key) 
        #devuelve el mensaje en un array con el size del string de cantidad de caracteres
        #por lo tanto ya no es necesario volver a utilizar la funcion ord
        encriptadoF2 =fn2(encriptadoF1,key)
        encriptadoF3 = fn3(encriptadoF2,key)
        encriptadoF4 = fn4(encriptadoF3,key)
        return encriptadoF4
    def combinacion2(mensaje,key):
        mensajeASCII = [ord(c) for c in mensaje]
        encriptadoF1 = fn1(mensajeASCII,key) 
        encriptadoF2 =fn2(encriptadoF1,key)
        encriptadoF4 = fn4(encriptadoF2,key)
        encriptadoF3 = fn3(encriptadoF4,key)
        return encriptadoF3
    def combinacion3(mensaje,key):
        mensajeASCII = [ord(c) for c in mensaje]
        encriptadoF4 = fn4(mensajeASCII,key) 
        encriptadoF2 =fn2(encriptadoF4,key)
        encriptadoF1 = fn1(encriptadoF2,key)
        encriptadoF3 = fn3(encriptadoF1,key)
        return encriptadoF3
    def combinacion4(mensaje,key):
        mensajeASCII = [ord(c) for c in mensaje]
        encriptadoF3 = fn3(mensajeASCII,key)
        encriptadoF2 = fn2(encriptadoF3,key)
        encriptadoF1 = fn1(encriptadoF2,key)
        encriptadoF4 = fn4(encriptadoF1,key)
        return encriptadoF4
    def desenCombinacion1(mensajeEncriptado,key):
        desencriptadoF4 = fn4D(mensajeEncriptado,key)
        desencriptadoF3 = fn3D (desencriptadoF4,key)
        desencriptadoF2 = fn2D (desencriptadoF3,key)
        desencriptadoF1 = fn1D (desencriptadoF2,key)
        mensaje_desencriptado = desencriptadoF1
        mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
        return mensaje_desencriptado
    def desenCombinacion2(mensajeEncriptado,key):
        desencriptadoF3 = fn3D(mensajeEncriptado,key)
        desencriptadoF4 = fn4D (desencriptadoF3,key)
        desencriptadoF2 = fn2D (desencriptadoF4,key)
        desencriptadoF1 = fn1D (desencriptadoF2,key)
        mensaje_desencriptado = desencriptadoF1
        mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
        return mensaje_desencriptado
    def desenCombinacion3(mensajeEncriptado,key):
        desencriptadoF3 = fn3D(mensajeEncriptado,key)
        desencriptadoF1 = fn1D (desencriptadoF3,key)
        desencriptadoF2 = fn2D (desencriptadoF1,key)
        desencriptadoF4 = fn4D (desencriptadoF2,key)
        mensaje_desencriptado = desencriptadoF4
        mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
        return mensaje_desencriptado
    def desenCombinacion4(mensajeEncriptado,key):
        desencriptadoF4 = fn4D (mensajeEncriptado,key)
        desencriptadoF1 = fn1D (desencriptadoF4,key)
        desencriptadoF2 = fn2D (desencriptadoF1,key)
        desencriptadoF3 = fn3D (desencriptadoF2,key)
        mensaje_desencriptado = desencriptadoF3 
        mensaje_desencriptado = ''.join(chr(i) for i in mensaje_desencriptado)
        return mensaje_desencriptado
    def obtener_bits_menos_significativos(s):
    # Convertir string a bits
        bits = ''.join(format(ord(i), '08b') for i in s)
        
        # Obtener los 4 bits menos significativos
        bits_menos_significativos = bits[-4:]
        
        return bits_menos_significativos
    