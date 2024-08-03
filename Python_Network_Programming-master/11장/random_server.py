#랜덤 넘버 서버프로그램

import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP 소켓
address = ("", 5000) #주소
s.bind(address) #소켓과 주소 결합
s.listen(5) #접속 대기
print('Waiting for requests...')

while True:
    client, addr = s.accept() #연결
    print("Connection requested from ", addr)

    num = random.randint(1,100)
    print("Sending {}".format(num))
    client.send(str(num).encode()) #임의 값 전송
    client.close()
