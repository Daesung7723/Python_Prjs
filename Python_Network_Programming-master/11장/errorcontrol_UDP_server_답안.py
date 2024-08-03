# 전송 손실을 가정한 UDP 서버 프로그램

import random
from socket import *

port = 2500
BUFFER = 1024
ErrorRate = 3
s_sock = socket(AF_INET, SOCK_DGRAM)
s_sock.bind(('', port))
print('Waiting for data')

while True:
    data, address = s_sock.recvfrom(BUFFER)
    if random.randint(1, 10) <= Errorrate: #패킷 손실
        print(f'Bad! Packet from {address} lost!!!')
        s_sock.sendto('NAK'.encode(), address) #NAK 응답 전송
    else:
        print(f'Good! Message is {data.decode()!r} from {address}') #메시지 출력
        s_sock.sendto('ACK'.encode(), address) #ACK 응답 전송