# 소켓을 이용한 블루투스 클라이언트 프로그램

import socket

serverMACAddress = 'B8:27:EB:2A:D1:45' #서버 MAC 주소
port = 3
s = socket.socket(socket.AF_BLUETOOTH,
                  socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))

while True:
    text = input() #송신 메시지
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
    
s.close()