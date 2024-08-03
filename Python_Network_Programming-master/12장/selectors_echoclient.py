#selectors 모듈을 이용한 TCP 클라이언트 프로그램

import selectors
import socket

sel = selectors.DefaultSelector()
keep_running = True
sendingmsg = [
    '두 번째 송신 메시지입니다',
    '첫 번째 송신 메시지입니다',
]
bytes_sent = 0
bytes_received = 0

# 연결 동작은 블록킹 모드이므로 연결 후에 비블록모드로 설정해야 한다
server_address = ('localhost', 5500)
print('연결 {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False) #반드시 넌블록킹 모드로 설정

# 읽기와 쓰기 이벤트를 모니터링하도록 이벤트 관리기(selector) 설정
# 각 이벤트가 발생하는 경우가 하나뿐이므로 콜백을 지정하지 않아도 된다
sel.register(
    sock,
    selectors.EVENT_READ | selectors.EVENT_WRITE,
)

while keep_running:
    print('\n입출력 대기')
    for key, mask in sel.select(timeout=1):
        e_sock = key.fileobj #이벤트가 발생한 소켓
        c_address = e_sock.getpeername() #장치의 주소 확인
        print('클라이언트({})'.format(c_address))

        if mask & selectors.EVENT_READ: #이벤트가 READ인지 확인
            print('  읽기 준비')
            data = e_sock.recv(1024) #소켓에서 데이터 읽기
            if data:
                # 읽기 이벤트 발생 소켓에서 데이터를 읽은 경우
                print('  수신 메시지 {}'.format(data.decode()))
                bytes_received += len(data)

            # data가 없으면 실행 종료
            keep_running = not (
                data or
                (bytes_received and
                 (bytes_received == bytes_sent))
            )

        if mask & selectors.EVENT_WRITE: #이벤트가 WRITE인지 확인
            print('  쓰기 준비')
            if not sendingmsg: #송신 메시지가 없으면
                print('  수신 모드로 전환')
                sel.modify(sock, selectors.EVENT_READ)
            else:
                # 메시지 송신
                send_msg = sendingmsg.pop()
                print('  전송 {!r}'.format(send_msg))
                sock.sendall(send_msg.encode())
                bytes_sent += len(send_msg)

print('종료')
sel.unregister(e_sock)
e_sock.close()
sel.close()
