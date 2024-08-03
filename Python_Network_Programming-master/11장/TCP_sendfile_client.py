# 파일 전송 프로그램

import socket

port = 2500
sock = socket.socket()
host = "localhost"

sock.connect((host, port))
msg = sock.recv(1024) #준비 완료 수신
print(msg.decode())

filename = input('File name to send(c:/test/sample.bin): ') #'\'대신 '/' 사용하여 경로 구분
filename = filename.strip('"')
print(f"Sending '{filename}'")

sock.sendall(filename.encode()) #파일 이름 전송

with open(filename, 'rb') as f:
    sock.sendfile(f,0) #파일 내용 전송
    
    #data = f.read()
    #while data:
    #    c_sock.sendall(data)
    #    data = f.read()
    
print('Sending complete')
sock.close()
