#select와 queue 모듈을 이용한 에코 서버 프로그램

import select, socket, queue

s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sock.setblocking(0) #블록킹 모드
s_sock.bind(('localhost', 2500))
s_sock.listen(5)

r_socks = [s_sock] #수신 소켓 목록. 서버 소켓 추가
w_socks = [] #송신 소켓 목록
msgQueues = {}#메시지 큐의 목록 {소켓: 메시지큐}

while r_socks:
    readEvent, writeEvent, errorEvent = select.select(
        r_socks, w_socks, r_socks)
    
    for s in readEvent: #읽기 가능 소켓 조사
        if s is s_sock: #서버 소켓인가?
            c_sock, c_address = s.accept()
            c_sock.setblocking(0) #블록킹 모드
            r_socks.append(c_sock) #클라이언트 수신 소켓 목록에 추가
            msgQueues[c_sock] = queue.Queue() #큐 생성
            
        else: #클라이언트 소켓인가?
            data = s.recv(1024)
            if data: #수신 데이터가 있으면
                msgQueues[s].put(data) #수신 메시지를 큐에 저장
                if s not in w_socks: #새로운 소켓이면 송신 소켓 목록에 추가
                    w_socks.append(s)
            else: #수신 데이터가 없으면
                if s in w_socks:
                    w_socks.remove(s) #송신 소켓 목록에서 제거
                r_socks.remove(s) #수신 소켓 목록에서 제거
                s.close()
                del msgQueues[s] #메시지 큐 제거

    for s in writeEvent: #쓰기 가능 소켓 조사
        try:
            next_msg = msgQueues[s].get_nowait() #메시지 큐에서 메시지 인출
        except queue.Empty: #큐가 비었으면
            w_socks.remove(s) #송신 소켓 목록에서 제거
        else: 
            s.send(next_msg) #인출된 메시지 전송

    for s in errorEvent: #오류 발생 소켓 조사
        r_socks.remove(s) #수신 소켓 목록에서 제거
        if s in w_socks:
            w_socks.remove(s)#송신 소켓 목록에서 제거
        s.close()
        del msgQueues[s] #해당 소켓의 메시지 큐 제거