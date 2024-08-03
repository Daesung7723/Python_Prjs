# 문자열 주소로부터 IP 주소 찾는 프로그램

import socket

HOSTS = [
    'www.uou.ac.kr',
    'www.dongyang.ac.kr',
    'www.python.org',
    'testname',
]

for host in HOSTS:
    try:
        print('{} : {}'.format(host, socket.gethostbyname(host)))
    except socket.error as msg:
        print('{} : {}'.format(host, msg))
