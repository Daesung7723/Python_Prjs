# 파일 전송 프로그램

import socket, os

port = 2500
s_sock = socket.socket()
host = ""
s_sock.bind((host, port))
s_sock.listen(1)

print('Waiting for connection....')

c_sock, addr = s_sock.accept() #클라이언트와 연결
print('Connected from', addr)
msg = c_sock.recv(1024) #클라이언트로부터 준비 완료 수신
print(msg.decode())
drv = input('Drive to seach: ')
os.startfile(drv+':/')
filename = input('File name to send(c:/test/sample.bin): ') #'\'대신 '/' 사용하여 경로 구분
print(f"Sending '{filename}'")

c_sock.sendall(filename.encode()) #파일 이름 전송

with open(filename, 'rb') as f:
    #c_sock.sendfile(f,0) #파일 내용 전송
    
    data = f.read()
    while data:
        c_sock.sendall(data)
        data = f.read()
    
print('Sending complete')
c_sock.close()
