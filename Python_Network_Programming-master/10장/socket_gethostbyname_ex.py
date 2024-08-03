# 문자열 주소로부터 확장 IP주소 찾는 프로그램

import socket
HOSTS = ['www.dongyang.ac.kr', 'pymotw.com','www.python.org','testname',]
for host in HOSTS:
    print(host)
    try:
        hostname, aliases, addresses = socket.gethostbyname_ex(host)
        print(' Hostname:', hostname)
        print(' Aliases :', aliases)
        print(' Addresses:', addresses)
    except socket.error as emsg:
        print('ERROR:', emsg)
    print()