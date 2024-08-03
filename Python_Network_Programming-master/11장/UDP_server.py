# UDP 에코 서버 프로그램

import socket
port = 2500
maxsize = 1024

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP 소켓
sock.bind(('', port))
print("수신 대기 중")

while True:
    data, addr = sock.recvfrom(maxsize) #데이터와 상대방 종단점 주소 수신
    print("Received message: ", data.decode())
    print(addr)

    sock.sendto(data,addr) #재전송
