# threading 모듈을 이용한 UDP 클라이언트 프로그램
# 데이터 수신은 스레드로 실행하고 송신은 무한 루프로 실행

import socket
import threading

def handler(sock): #스레드로 실행할 함수
    while True: #데이터 수
        try:
            msg, addr = sock.recvfrom(1024)
        except: #수신 데이터가 없으면 다시 시도
            continue
        else: #수신 메시지가 있으면 출력
            print(msg.decode())

conn = ('localhost', 2500)
svr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_id = input("ID를 입력하세요: ")

cThread = threading.Thread(target=handler, args=(svr,)) #스레드 생성
cThread.daemon = True
cThread.start() #스레드 시작
svr.sendto(''.encode(), conn) # 클라이언트 등록

while True:
    msg = '['+my_id+'] '+input()
    svr.sendto(msg.encode(), conn)