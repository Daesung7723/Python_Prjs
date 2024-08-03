#socket_getaddrinfo.py
import socket

def get_constants (prefix ):
    """
    소켓 모듈의 속성값을 속성문자와 맵핑시키는 디셔너리를 만든다 {속성값: 속성문자}
    """
    return {
        getattr(socket, n):n # 속성값(getattr())과 속성문자(n) 딕셔너리
        for n in dir(socket) # socket의 속성문자
        if n.startswith(prefix) #속성문자가 prefix로 시작하는지 조사
    }

families =get_constants ('AF_') #'AF_'로 시작하는 속성문자
types =get_constants ('SOCK_') #'SOCK_'으로 시작하는 속성문자
protocols =get_constants ('IPPROTO_') #'IPPROTO_'로 시작하는 속성문자

for response in socket.getaddrinfo('www.dongyang.ac.kr','http'):

    # 5-튜플 응답을 unpacking한다
    family ,socktype ,proto ,canonname ,sockaddr =response

    print ('Family        :',families[family]) #주소 유형
    print ('Type          :',types[socktype]) #소켓 유형
    print ('Protocol      :',protocols[proto]) #전송 프로토콜
    print ('Canonical name:',canonname) #호스트 정식명칭
    print ('Socket address:',sockaddr) #주소와 포트번호
    print ()