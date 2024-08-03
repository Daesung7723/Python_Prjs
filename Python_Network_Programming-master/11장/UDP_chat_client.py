# UDP 채팅 클라이언트 프로그램

import socket
BUFFSIZE = 1024
port = 2500

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.5)
ip_addr = input('Server IP Address: ')
if ip_addr == '':
    ip_addr = 'localhost'
addr = (ip_addr, port)

while True:
    msg = input("<- ")
    sock.sendto(msg.encode(),addr)
    
    try:
        data, addr = sock.recvfrom(BUFFSIZE)
    except:
        continue
    else:
        print("-> ", end ='')
        print(data.decode())
