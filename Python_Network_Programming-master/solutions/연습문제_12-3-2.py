#GUI_socket_multiserver.py

import threading
import sys
from socket import *

ECHO_PORT = 2500
BUFSIZE = 2048

def convertC2F(sock):
    while True:
        print("waiting ...")
        data = sock.recv(BUFSIZE)
        if not data:
            print("Remote connection close")
            sock.close()
            break
        data = float(data.decode()) #수신 데이터를 float형으로 변환
        data = 9.0/5.0*data + 32.0 #화씨 온도 계산
        print("Temp: {:.1f}".format(data))
        data = '{:.1f}'.format(data)
        data = str(data).encode()
        sock.send(data)

port = ECHO_PORT
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', port))

s.listen(5)
print("Waiting for connection from client")

while True:   
    conn, (remotehost, remoteport) = s.accept() #클라이언트를 연결하고
    print('connected by', remotehost, remoteport)
    th = threading.Thread(target=convertC2F, args=(conn,)) #스레드 생성하여 실행
    th.daemon = True
    th.start()
