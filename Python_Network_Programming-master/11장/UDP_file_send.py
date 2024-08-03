#UDP 파일 송신 프로그램(클라이언트)

import socket, time, sys

BUFSIZE = 1024*16
addr = ('localhost', 2500) #서버(수신) 주소
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file_name = input("File name to send: ")
sock.sendto(file_name.encode(), addr) #파일 이름 전송
resp, client = sock.recvfrom(BUFSIZE) #응답 수신

if resp.decode().lower() == 'ok': #'ok' 응답 수신
    fp = open(file_name, "rb") #송신 파일 열기
    data = fp.read(BUFSIZE) #파일 송신
    print("송신 중...")
    
    while(data): #읽은 내용이 없으면 data = ""(False)
        sock.sendto(data, client)
        time.sleep(0.2) #수신할 때까지 잠시 대기
        data = fp.read(BUFSIZE)
        
else:
    print("The remote does not respond")
    sys.exit() #프로그램 종료

#송신 완료를 위해 빈 데이터 전송
#상대방은 빈 데이터를 받으면 전송 종료로 인식
sock.sendto(data, client) 
fp.close()
print("전송 완료")    