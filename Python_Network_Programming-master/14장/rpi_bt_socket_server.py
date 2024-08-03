# 소켓을 이용한 블루투스 서버 프로그램

import socket

hostMACAddress = 'B8:27:EB:2A:D1:45' # 서버의 블루투스 MAC 주소
port = 3 # 임의로 설정 가능하나 클라이언트 포트 번호와 일치해야 함
backlog = 1
size = 1024

#소켓 생성
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

try: #연결
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except: #연결 실패
    print("Closing socket") 
    client.close()
    s.close()