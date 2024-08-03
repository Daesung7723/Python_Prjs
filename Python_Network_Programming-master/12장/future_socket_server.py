# concurrent.futures 모듈을 이용한 멀티 에코 서버 프로그램

import concurrent.futures as cf
from socket import *

def receive_message(sock, address):
    while True:
        try:
            r_msg = sock.recv(1024) #메시지 수신
            if not r_msg: #상대방이 연결을 종료함
                break
            print('수신 메시지: ', r_msg.decode())
            sock.sendall(r_msg) #에코
            print('송신 메시지: ', r_msg.decode())
        except: #강제로 연결이 종료됨
            break
    sock.close()
    
s_sock = socket(AF_INET, SOCK_STREAM)
s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s_sock.bind(('', 2500))
s_sock.listen(5)
print('{}에서 연결 대기 중'.format(s_sock.getsockname()))

#스레드 풀을 생성하고 함수를 등록한다
with cf.ThreadPoolExecutor(max_workers=10) as th: 
    try:
        while True: #다중 접속을 받는다
            c_sock, addr = s_sock.accept()
            print("Connectionn from", addr)
            th.submit(receive_message, c_sock, addr) #스레드 풀에 등록한다
    except: #예외가 발생하면 종료한다
        pass
    finally:
        s_sock.close()
