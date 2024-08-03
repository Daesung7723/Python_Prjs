# UDP 채팅 서버 프로그램

import socket
import time

host = ''
port = 2500

clients = [] #클라이언트 리스트

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

print('Server Started')

while True:
    try:
        data, addr = s.recvfrom(1024) #수신 데이터가 없으면 반복 시도
        if "quit" in data.decode():
            if addr in clients:
                clients.remove(addr)
                print(f'{addr}가 떠났습니다')
        if addr not in clients: #클라이언트 리스트에 없으면 추가
            print("new client")
            clients.append(addr)
        print(time.ctime(time.time()) + str(addr) + ': :' + data.decode())
        for client in clients: #모든 클라이언트에게 전송
            if client != addr and data:
                s.sendto(data, client)
    except:
        pass
s.close()