# 오류제어 기능이 포함된 UDP 클라이언트(전송) 프로그램

from socket import *

port = 2500
BUFFER = 1024
server = "localhost"
c_sock = socket(AF_INET, SOCK_DGRAM)
c_sock.connect((server, port))

total_delay = 0 # total delay time for 10 trials

for i in range(10): #10번 시도
    delay = 0.1  #0.1초부터 대기 시작
    sub_total = 0 # total delay time for one trial
    data = 'Hello message ' + str(i)

    while True:
        print("\nSending:", data)
        c_sock.send(data.encode())
        print(f'Waiting up to {delay} seconds for a reply')
        c_sock.settimeout(delay) #타임아웃 설정
        
        try:
            resp = c_sock.recv(BUFFER) #데이터 수신
            
        except timeout: #타임아웃 발생
            print("No response!!!")
            delay *= 2  #대기 시간 2배 증가
            if delay > 2.0: #시간 초과
                print('The server seems to be down')
                break
            
        else:
            sub_total += delay 
            print(resp.decode(), "received")
            break #종료
        
    total_delay += sub_total

print(f"Average Delay Time={total_delay/10.:.2f}") # average delay time
