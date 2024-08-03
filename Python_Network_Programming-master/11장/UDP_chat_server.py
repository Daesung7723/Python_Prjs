# UDP 채팅 서버 프로그램

import socket

port = 2500
maxsize = 1024
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', port))

print("Waiting for client")
while True:
    print("<- ", end ='')
    data, addr = sock.recvfrom(maxsize)
    print(data.decode())
    #print(addr)
    resp = input("-> ")
    sock.sendto(resp.encode(),addr)
