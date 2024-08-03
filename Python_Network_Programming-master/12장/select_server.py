#select를 이용한 TCP 멀티 에코 서버

import socket, select

if __name__=="__main__":
    socks = [] #읽기 가능 소켓 목록
    BUFFER = 1024
    port = 2500
    
    s_sock = socket.socket() #TCP socket
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_sock.bind(('', port))
    s_sock.listen(5)

    #listener 소켓을 소켓 목록에 추가
    socks.append(s_sock) 
    print(str(port) + "에서 접속 대기 중 ")

    while True:
        #연결 요청 및 수신 대기(읽기 가능 이벤트만 조사)
        r_sock, _, _ = select.select(socks, [], [], 0)

        for s in r_sock: #수신 소켓 리스트의 소켓 조사
            if s == s_sock: #연결 요청인가?
                c_sock, addr = s_sock.accept() #새로운 클라이언트 연결
                socks.append(c_sock) #연결된 소켓을 소켓 리스트에 추가
                print(" Client (%s, %s) connectd" %addr)
                
            else: #데이터 수신
                try: #연결되지 않았으면 예외가 발생할 수 있으므로 try로 처리
                    data = s.recv(BUFFER) #데이터 수신
                    print("Received: ", data.decode())
                    if data:
                        s.send(data) #수신 데이터를 다시 전송
                        
                except: #연결되지 않아 수신 데이터가 없음
                    print("Client (%s, %s) is offline" %addr)
                    s.close()
                    socks.remove(s) #연결 종료된 소켓을 목록에서 제거
                    continue
                
    s_sock.close()