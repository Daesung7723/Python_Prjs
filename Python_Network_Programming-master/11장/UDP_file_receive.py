#UDP 파일 수신 프로그램(서버)

import socket

BUFSIZE = 1024*16

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('', 2500)
sock.bind(addr)

file_name, client = sock.recvfrom(BUFSIZE) #파일 이름 수신
sock.sendto('ok'.encode(), client) #'ok' 응답

with open('d:/'+file_name.decode(), "wb") as fp: #파일을 수신하여 저장
    print("파일 수신 중...")
    while True:
        data, addr = sock.recvfrom(BUFSIZE)
        if not data: #빈 데이터를 받으면 수신 완료
            break
        fp.write(data) #수신 데이터를 파일에 저장
    
print("수신 완료")