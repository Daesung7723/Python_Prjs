# select 모듈을 이용한 TCP 클라이언트 프로그램

from socket import *
from select import *
import time

socks = []
sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socks.append(sock) #생성된 소켓을 목록에 추가
sock.connect(('localhost', 2500)) #서버 연결

while True:
    r_sock, _, _ = select(socks,[],[], 0) #넌블록킹 모드
    #time.sleep(1)
    if r_sock: #읽기 가능 이벤트 발생
        for s in r_sock:
            if s == sock: #자신에게 온 데이터인가?
                msg = sock.recv(1024).decode()
                print("수신 메시지:", msg)
    smsg = input("전송 메시지: ")
    sock.sendall(smsg.encode())
