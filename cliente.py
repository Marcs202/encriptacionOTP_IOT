# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 19:17:25 2024

@author: marco
"""
from twisted.internet import  DataGramProtocol
from twisted.internet import reactor
from random import randit


class Client (DataGramProtocol):
    def __init__ (self,host, port):
        if host == "localhost":
            host = "127.0.0.1"
            
        self.id = host, port
        self.addres = None
        print("Escuchando en el puerto: ", self.id)
        
    def datagramReceived(self, datagram, addr):
        print (addr, ":", datagram)
    
    def send_message(self):
        while True:
            self.transport.write(input(":::").encode('utf-8'),self.addres)
            
if __name__ == '__main__':
    port = randit(1000,5000)
    reactor.listUDP(port, Client("localhost", port))
    