#create_connection()을 이용한 TCP 클라이언트 프로그램

import socket

# TCP 소켓 생성과 연결
sock =socket.create_connection(('localhost',2500 ))

# 메시지 전송
message ="클라이언트 메시지"
print('sending: {}'.format (message))
sock.sendall(message.encode())

data =sock.recv(1024) #데이터 수신
print('received: {}'.format (data.decode()))
print('closing socket')
sock .close () #연결 종료
