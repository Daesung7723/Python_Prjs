#사용자 정의 모듈을 이용한 에코 서버 프로그램

import sys
#sys.path.append("G:\파이썬교재\sources\book_codes\3판\common")
import MyTCPServer as ms#사용자 정의 모듈을 불러온다

server = ms.TCPServer(2500)
print("Waiting for connection")
while True:
    if not server.connected:
        server.accept()
    else:
        msg = server.receive()
        # 연결이 되어 있지 않으면 None이 반환됨
        if msg:
            print('수신메시지: ', msg)
            server.send(msg)
        else:
            print("Disconnected")
            break
server.disconnect()
