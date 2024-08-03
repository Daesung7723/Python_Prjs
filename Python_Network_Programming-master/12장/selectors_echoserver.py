#slectors 모듈을 이용한 TCP 에코 서버 프로그램

import selectors
import socket

#기본 이벤트 관리기 선택
sel = selectors.DefaultSelector()

def accept(sock, mask):
    c_sock, addr = sock.accept()  # 연결 수락
    print(f'{addr}에서 연결됨')
    c_sock.setblocking(False) #소켓은 넌블록킹 모드로 설정되어야 한다
    
    #연결 후에 읽기 이벤트가 발생하면 read() 함수를 실행하도록 설정
    sel.register(c_sock, selectors.EVENT_READ, read) 

def read(c_sock, mask):
    try:
        data = c_sock.recv(1024)  # 데이터 수신
    except:
        print("연결 종료")
        sel.unregister(c_sock)
        c_sock.close()
        return
    if data:
        print('수신데이터: ', data.decode())
        c_sock.send(data)  # 송신자에게 재전송
    else:
        print(f'{c_sock} 소켓 닫음')
        sel.unregister(c_sock) #연결 종료
        c_sock.close()

sock = socket.socket()
sock.bind(('', 5500))
sock.listen(5)
sock.setblocking(False) #넌블록킹 모드로 동작

#처음 읽기 이벤트(연결 요청)가 발생하면 accept() 함수를 실행하도록 설정
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select(timeout=0) #이벤트 발생 대기
    
    #발생 이벤트를 조사하여 콜백 호출
    for key, mask in events:
        #sel.select()가 반환하는 key 객체의 data 속성은 콜백함수이다
        callback = key.data
        #key 객체의 fileobj 속성은 소켓이고, mask는 발생 이벤트이다
        callback(key.fileobj, mask) #콜백함수 호출