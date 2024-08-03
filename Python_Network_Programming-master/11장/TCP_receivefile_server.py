# 파일 수신 프로그램

import socket, os, sys

s_sock = socket.socket()
host = ""
port = 2500

s_sock.bind((host, port))
s_sock.listen(5)

while True:
    print("Waiting for client")
    c_sock, addr = s_sock.accept()
    c_sock.send("I am ready".encode())
    fn = c_sock.recv(1024).decode() # 경로를 포함한 파일이름 수신
    filename = os.path.basename(fn) # 기본 파일이름 추출

    with open('d:/temp/'+filename, 'wb') as f: #저장 파일 열기
        #print('file opened')
        print(f'receiving {filename}')
        while True:
            data = c_sock.recv(8192) #파일 내용 수신
            if not data: #내용이 없으면 종료
                break
            f.write(data)#내용을 파일에 쓰기

    print('Download complete\n')
    c_sock.close()
    #print('Connection closed')
