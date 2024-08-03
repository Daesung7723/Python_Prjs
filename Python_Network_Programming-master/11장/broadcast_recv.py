# 브로트캐스트 수신 프로그램

import select, socket 

port = 1060  
bufferSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
s.setblocking(0)

while True:
    result = select.select([s],[],[]) #비동기 데이터 수신
    msg = result[0][0].recvfrom(bufferSize) #데이터 읽기
    print(msg[0].decode())
