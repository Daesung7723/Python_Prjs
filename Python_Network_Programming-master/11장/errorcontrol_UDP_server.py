# 전송 손실을 가정한 UDP 서버 프로그램

import random
from socket import *

port = 2500
BUFFER = 1024
ErrorRate = 4

s_sock = socket(AF_INET, SOCK_DGRAM)
s_sock.bind(('', port))
print('Waiting for data')

while True:
    data, address = s_sock.recvfrom(BUFFER)
    if random.randint(1, 10) < ErrorRate: #패킷 손실
        print(f'Packet from {address} lost!!!')
        
    else:
        print(f'Message is {data.decode()} from {address}') #메시지 출력
        s_sock.sendto('ACK'.encode(), address) #ACK 응답 전송