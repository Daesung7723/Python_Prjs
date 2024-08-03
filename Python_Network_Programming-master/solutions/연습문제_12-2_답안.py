#threading.Thread를 이용한 TCP client program
#Thread_TCP_client.py

import socket
import threading
def handler(sock):
    while True:
        data = sock.recv(1024)
        #print('\nreceived: ',data.decode())
        print(data.decode())
        
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Server Address(default=127.0.0.1): ")
if host == '':
    host = 'localhost'
sock.connect((host, 2500))
cThread = threading.Thread(target=handler, args=(sock,))
cThread.daemon = True
cThread.start()

name = ''
while not name:
    name = input("당신의 이름은? ")
    
while True:
    #msg = input('> ')
    msg = input()
    sock.send((name + ': ' + msg).encode())
