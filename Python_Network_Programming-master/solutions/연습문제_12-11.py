#selectors 모듈을 이용한 TCP 클라이언트 프로그램

import selectors
import socket

def write(sock, mask):
    if not sendingmsg:
        # 송신 메시지가 없으면 수신 모드로 전환
        sel.modify(sock, selectors.EVENT_READ, read)
    else:
        send_msg = sendingmsg.pop() # 마지막 요소부터 전송
        print("송신 메시지:", send_msg)
        sock.sendall(send_msg.encode())
        # 메시지를 전송하고 수신 모드로 번환
        sel.modify(sock, selectors.EVENT_READ, read)

def read(sock, mask):
    try:
        data = sock.recv(1024)  # 데이터 수신
    except:
        print("연결 종료")
        sel.unregister(sock)
        sock.close()
    
    if data:
        print('수신데이터: ', data.decode())
        
    # 데이터 수신 후 송신 모드로 전환
    sel.modify(sock, selectors.EVENT_WRITE, write) 

        
sel = selectors.DefaultSelector()
sendingmsg = [
    '세 번째 송신 메시지입니다',
    '두 번째 송신 메시지입니다',
    '첫 번째 송신 메시지입니다'
]

# 연결 동작은 블록킹 모드이므로 연결 후에 비블록모드로 설정해야 한다
server_address = ('localhost', 2500)
print('연결: {}, port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False) #반드시 넌블록킹 모드로 설정

# 읽기와 쓰기 이벤트를 모니터링하도록 이벤트 관리기(selector) 설정
sel.register(sock, selectors.EVENT_WRITE, write)

while True:
    for key, mask in sel.select():
        callback = key.data
        callback(key.fileobj, mask)
