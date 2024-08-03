#멀티캐스트 수신 프로그램

from socket import *
import struct

BUFFER = 1024
group_addr = "224.0.0.255" #그룹 주소
#group_addr = "224.3.29.71"
r_sock = socket(AF_INET, SOCK_DGRAM)
r_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
r_sock.bind(("", 5005))

mreq = struct.pack("4sL", inet_aton(group_addr), INADDR_ANY)
r_sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq) #멤버 가입
print("Ready to receive")

while True:
    rmsg, addr = r_sock.recvfrom(BUFFER) #메시지 수신
    print("Received '{}' from ({}, {})".format(rmsg.decode(), *addr))
    r_sock.sendto('ACK'.encode(), addr) #ACK 전송