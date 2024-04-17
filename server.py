import socket
import pickle
import select
import random
import sympy
import time 
from generador_keys import GeneracionLlaves
from encriptacion_combinada import Encriptacion
def generate_random_prime(bits):
    while True:
        # Generar un número aleatorio de 64 bits
        num = random.getrandbits(bits)
        
        # Asegurar que el número sea impar
        num |= (1 << bits - 1) | 1
        
        # Verificar si el número es primo
        if sympy.isprime(num):
            return num

# Generar un número primo de 64 bits
def emparejar(conn,received_messages,p,s ):
    ready = select.select([conn], [], [], 0.0)
    if ready[0]:
        data = conn.recv(1024)
        if data:
            #si cliente inicio el FCM
            data_arr = pickle.loads(data)
            received_messages.append(data_arr)
            p = received_messages[0][0]
            s = received_messages[0][1]
            print("El numero p del client es: ", p)
            print("El numero s del client es: ", s)
            print("Enviando primo Q")
            q= generate_random_prime(64)
            data_string =pickle.dumps(q)
            conn.send(data_string)
            received_messages.clear()
            lista = [q,p,s]
            return lista
            
    else:
            #inicia la conexion el server
            #por propiedades de la conexion de socket si el server inicia
            # el fcm ready sera false por lo tanto empieza aca
            print("Enviando mensaje FCM") 
            primosPS = [generate_random_prime(64),generate_random_prime(64)]
            data_string =pickle.dumps(primosPS)
            conn.send(data_string)
            lista = [0,primosPS[0],primosPS[1]]
            return lista
def enviarMensaje(conn,mensajeEncriptado):
    data_string = pickle.dumps(mensajeEncriptado)
    conn.send(data_string)
def start_server():
    
    psn=""
    p=0
    q=0
    s=0
    host = 'localhost'
    port = 12345
    received_messages = []

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    generadorLlaves = GeneracionLlaves
    encriptador = Encriptacion
    contador = 0
    print("Conexión desde: " + str(address))
    while True:
        print("\n\t1. Emparejar (FCM)")
        print("\t2. Enviar mensaje (RM)")
        print("\t3. Leer mensajes")
        print("\t4. Generar nuevas llaves (KUM)")
        print("\t5. Salir (LCM)")
        option = input("Elige una opción: ")
        if option == '1':
            resultEmparejamiento = emparejar(conn,received_messages,p,s)
            if resultEmparejamiento[0] == 0: #si es 0, la conexion la empieza el server, ´por lo tanto q entra 
                data = conn.recv(1024)
                data_arr = pickle.loads(data)
                received_messages.append(data_arr)
                q  = received_messages[0]
                p = resultEmparejamiento[1]
                s = resultEmparejamiento[2]
                print ("El valor de Q recibido de cliente es: ", q)
                
            else:#si no es 0  es porque cliente empezo el FCM, y q se genera en server
                q = resultEmparejamiento[0]
                p = resultEmparejamiento[1]
                s = resultEmparejamiento[2]
                print ("El valor de Q generado en server es: ", q) 
            
            keys= generadorLlaves.generate_keys(p,q,s,50)  
            for i, key in enumerate(keys):
                print(f"Key {i+1}: {key}")
            received_messages.clear()
        elif option == '2': 
            mensaje_encriptado=""
            mensaje = input("Ingrese el mensaje a encriptar: ")
            psn=encriptador.obtener_bits_menos_significativos(mensaje)
            if psn == '0000' or psn == '1111' or psn == '1110' or psn == '0001':
                mensaje_encriptado = encriptador.combinacion1(mensaje,keys[contador])
                
            elif psn == '0010' or psn == '1101' or psn == '0011' or psn == '1100':
                mensaje_encriptado = encriptador.combinacion2(mensaje,keys[contador])
                
            elif psn == '0100' or psn == '1011' or psn == '0101' or psn == '1010':
                mensaje_encriptado = encriptador.combinacion3(mensaje,keys[contador])
                
            elif psn == '0110' or psn == '0111' or psn == '1000' or psn == '1001':
                mensaje_encriptado = encriptador.combinacion4(mensaje,keys[contador])
                
            print("El mensaje encriptado es: ", mensaje_encriptado)
            print("El PSN de este mensaje es: ",psn)
            mensaje_encriptado.insert(0,psn)
            enviarMensaje(conn,mensaje_encriptado)
            llave_quemada = keys.pop(0)
            print("Llave eliminada: ", llave_quemada)
            contador+=1           
        elif option == '3':
            ready = select.select([conn], [], [], 0.0)
            if ready[0]:
                data = conn.recv(1024)
                if data:
                    data_arr = pickle.loads(data)
                    received_messages.append(data_arr)
                    mensaje_desencriptado=""
                    psn = received_messages[0][0]
                    mensajeSubList = received_messages[0]
                    mensaje = mensajeSubList[1:]
                    print  ("PSN recibido: ", psn )
                    print("Mensajes encriptado: ", mensaje)
                    
                    if psn == '0000' or psn == '1111' or psn == '1110' or psn == '0001':
                        mensaje_desencriptado = encriptador.desenCombinacion1(mensaje,keys[contador])
                    elif psn == '0010' or psn == '1101' or psn == '0011' or psn == '1100':
                        mensaje_desencriptado = encriptador.desenCombinacion2(mensaje,keys[contador])
                    elif psn == '0100' or psn == '1011' or psn == '0101' or psn == '1010':
                       mensaje_desencriptado = encriptador.desenCombinacion3(mensaje,keys[contador])
                    elif psn == '0110' or psn == '0111' or psn == '1000' or psn == '1001':
                        mensaje_desencriptado = encriptador.desenCombinacion4(mensaje,keys[contador])
                    print("El mensaje desencriptado es: ", mensaje_desencriptado)
                    print("El PSN de este mensaje es: ",psn)
                    received_messages.clear()
                    llave_quemada = keys.pop(0)
                    print("Llave eliminada: ", llave_quemada)
                    contador+=1
                else:
                    print("Bandeja de entrada vacia")
            else:
                print("No hay mensajes nuevos")
        elif option == '4':
            print ("Generar nuevas llaves")
            resultEmparejamiento = emparejar(conn,received_messages,p,s)
            if resultEmparejamiento[0] == 0: #si es 0, la conexion la empieza el server, ´por lo tanto q entra 
                data = conn.recv(1024)
                data_arr = pickle.loads(data)
                received_messages.append(data_arr)
                q  = received_messages[0]
                p = resultEmparejamiento[1]
                s = resultEmparejamiento[2]
                print ("El valor de Q recibido de cliente es: ", q)
                
            else:#si no es 0  es porque cliente empezo el FCM, y q se genera en server
                q = resultEmparejamiento[0]
                p = resultEmparejamiento[1]
                s = resultEmparejamiento[2]
                print ("El valor de Q generado en server es: ", q) 
            
            keys= generadorLlaves.generate_keys(p,q,s,50)  
            for i, key in enumerate(keys):
                print(f"Key {i+1}: {key}")
            received_messages.clear()
        elif option == '5':
            print(f"p: {p}\nq:{q}\ns: {s}")
            print("Borrando llaves y primos...")
            time.sleep(0.5)
            keys.clear()
            print (keys)
            break
        else:
            print("Opción no válida. Por favor, elige una opción del menú.")


    conn.close()

if __name__ == '__main__':
    start_server()
