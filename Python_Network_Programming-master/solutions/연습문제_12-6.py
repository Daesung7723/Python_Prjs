# multiprocessing 모듈을 이용한 TCP 서버 프로그램

from socket import socket
from multiprocessing import Process

def handle(sock): #자식 프로세스로 실행할 함수
    #문자를 수신하여 표시하고 다시 전송
    while True:
        msg = sock.recv(1024).decode()
        print(f'Received message: {msg}')    
        if msg.title() == "Hello":
            sock.send("Hello Client".encode())
        elif msg.title() == "Good":
            p2 = Process(target=handle2, args=(sock,))
            print("Process ID: ", p2.pid)
            p2.start()
        else:
            sock.send("Welcome".encode())
            
def handle2(sock):
    sock.send("Good Afternoon".encode())
    
    
if __name__ == "__main__":
    sock = socket()
    addr = ('', 2500)
    sock.bind(addr)
    sock.listen(4)
    
    while True:
        # 복수의 클라이언트 서비스
        c_sock, r_addr = sock.accept()
        print(f'{r_addr} is connected')
        p1 = Process(target=handle, args=(c_sock,)) #자식프로세스 생성
        p1.start()
