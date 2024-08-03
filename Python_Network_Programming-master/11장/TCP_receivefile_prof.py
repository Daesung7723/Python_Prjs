# 파일 수신 프로그램

import socket, os, sys

while True:
    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_sock.settimeout(1.0)
    #host = "localhost"
    host = input("서버 주소: ")
    port = 2500

    try:
        s_sock.connect((host, port)) #서버와 연결
    except:
        print("연결 실패")
        continue
    s_sock.send("I am ready".encode()) #준비 완료 메시지 송신
    fn = s_sock.recv(1024).decode() # 경로를 포함한 파일이름 수신
    filename = os.path.basename(fn) # 기본 파일이름 추출

    with open('d:/temp/'+filename, 'wb') as f: #저장 파일 열기
        print('file opened')
        print('receiving file...')
        while True:
            data = s_sock.recv(8192) #파일 내용 수신
            if not data: #내용이 없으면 종료
                break
            f.write(data)#내용을 파일에 쓰기

    print('Download complete')
    s_sock.close()
    print('Waiting files...')
