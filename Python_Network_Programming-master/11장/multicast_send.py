#멀티캐스트 송신 프로그램

from socket import *
import struct

group_addr = ("224.0.0.255", 5005) #그룹 주소
#group_addr = ('224.3.29.71', 10000)
s_sock = socket(AF_INET, SOCK_DGRAM) #UDP 소켓 사용
s_sock.settimeout(0.5)

TTL = struct.pack('@B', 2) #TTL 설정
s_sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, TTL)

while True:
    rmsg = input('Your message: ')
    s_sock.sendto(rmsg.encode(), group_addr) #멀티캐스트 메시지 전송
    
    while True:
        try:
            #모든 수신자로부터 응답 수신
            response, addr = s_sock.recvfrom(1024)
        except timeout: #타임아웃 예외 발생
            break
        else:
            #응답 출력
            print('{} from {}'.format(response.decode(), addr)) 
