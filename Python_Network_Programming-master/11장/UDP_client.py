# 간단한 UDP 클라이언트 프로그램

import socket
BUFFSIZE = 1024
port = 2500

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP 소켓
msg = "Hello UDP server"
sock.sendto(msg.encode(),('localhost', port)) #메시지 전송

while True:
    data, addr = sock.recvfrom(BUFFSIZE) #데이터 수신
    print("Server says:", data.decode())
    msg = input('Sending message: ')
    sock.sendto(msg.encode(), addr) #메시지 전송
