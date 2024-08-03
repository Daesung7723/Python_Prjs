# 브로드캐스트 수신 프로그램

from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 10000))

while True:
    msg, addr = s.recvfrom(1024)
    print(msg.decode())