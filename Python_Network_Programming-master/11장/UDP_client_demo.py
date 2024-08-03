# 간단한 UDP 클라이언트 프로그램

import socket
BUFFSIZE = 1024
port = 2500

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
msg = "Hello UDP server"
sock.sendto(msg.encode(),('localhost', port))
data, addr = sock.recvfrom(BUFFSIZE)
print("Server says:", data.decode())
