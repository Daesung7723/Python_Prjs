# select()를 이용한 다중 TCP 에코 서버
# 읽기 이벤트만 조사한다

import socket, select
import RPi.GPIO as GP

# setup GPIO pin numbering
GP.setmode(GP.BCM)
GP.setwarnings(False)
GP.setup(18, GP.OUT) #setup GPIO18 as OUT. LED connected
GP.setup(23, GP.IN) #setup GPIO23 as IN. Switch connected

sock_list = [] #이벤트 조사 소켓 목록
BUFFER = 1024
port = 2500

s_sock = socket.socket() #TCP 소켓
s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_sock.bind(('localhost', port))
s_sock.listen(5)

sock_list.append(s_sock) #서버 소켓을 목록에 추가
print("Server waiting on port " + str(port))

while True:
    r_sock, w_sock, e_sock = select.select(sock_list, [], [], 0) #감시 설정

    for s in r_sock: #읽기 이벤트 소켓 조사
        if s == s_sock: #서버 소켓?
            c_sock, addr = s_sock.accept()
            sock_list.append(c_sock) #클라이언트 소켓 목록 추가
            print(" Client (%s, %s) connectd" %addr)
        else: #클라이언트 소켓
            try:
                data = s.recv(BUFFER) #LED 제어
                if data.decode().upper() == "ON":
                    LED = 1
                else:
                    LED = 0
                GP.output(18, LED)
                
                SW = GP.input(23) #스위치 상태 읽기
                if SW == 1:
                    print("Switch is ON")
                else:
                    print("Switch is OFF")
                s.send(str(SW).encode()) #스위치 상태 전송
                time.sleep(2)
            
            except: #연결 종료됨
                print("Client (%s, %s) is offline" %addr)
                s.close()
                sock_list.remove(s) #연결이 종료된 소켓은 목록에서 제거
                continue
            
s_sock.close()
