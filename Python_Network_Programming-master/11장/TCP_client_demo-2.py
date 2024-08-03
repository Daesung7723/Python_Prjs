# 간단한 TCP 클라이언트 프로그램

import socket, sys

port = 2500
address = ("localhost", port)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
while True:
    msg = input("Message to send: ")
    if msg == 'n':
        s.close()
        break
    s.send(msg.encode()) #send a message to server
    r_msg = s.recv(BUFSIZE) #receive message from server
    if not r_msg: break
    print("Received message: %s" %r_msg.decode())
sys.exit()