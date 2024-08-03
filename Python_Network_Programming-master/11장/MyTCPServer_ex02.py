#사용자 정의 모듈을 이용한 에코 서버 프로그램

import sys
#sys.path.append("G:\파이썬교재\sources\book_codes\3판\common")
import MyTCPServer as ms#사용자 정의 모듈을 불러온다

#숫자에 대한 영어 사전
table = {'1':'one', '2': 'two', '3': 'three', '4': 'four',\
'5':'five', '6': 'six', '7': 'seven', '8': 'eight',\
'9': 'nine', '10': 'ten'}

server = ms.TCPServer(2500)
print("Waiting for connection")
while True:
    if not server.connected:
        server.accept()
        continue
    else:
        data = server.receive()
    try:
        resp = table[data] #데이터를 key로 사용하여 value를 가져온다
    except:
        server.send('Try again') #오류가 있을 때 
    else:
        server.send(resp) #변환 값을 전송
server.disconnect()
