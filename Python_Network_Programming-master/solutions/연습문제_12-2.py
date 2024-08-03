#threading.Thread를 이용한 TCP client program
#Thread_TCP_client.py

import socket
import threading


def handler(sock):
    
    while True:
        data = sock.recv(1024)
        print('\nreceived: ',data.decode())
        

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Server Address(default=127.0.0.1): ")
if host == '':
    host = 'localhost'
sock.connect((host, 2500))
cThread = threading.Thread(target=handler, args=(sock,))
cThread.daemon = True
cThread.start()

while True:
    msg = input('> ')
    sock.send(msg.encode())
