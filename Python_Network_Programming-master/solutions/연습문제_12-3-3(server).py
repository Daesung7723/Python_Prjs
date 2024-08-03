#GUI_socket_UDP_server.py

import sys
import struct
from socket import *

ECHO_PORT = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_DGRAM)
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(('', ECHO_PORT))
print("ready")

while True:
    data, r_addr = sock.recvfrom(BUFSIZE)
    if not data:
        break
    data = float(data.decode()) #수신 데이터를 float형으로 변환
    print('섭씨 ',data)
    data = 9.0/5.0*data + 32.0 #화씨 온도 계산
    data = '{:.1f}'.format(data)
    print('화씨 ',data)
    sock.sendto(data.encode(), r_addr)
sock.close()
