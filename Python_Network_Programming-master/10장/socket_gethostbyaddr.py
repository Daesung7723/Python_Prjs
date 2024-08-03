# IP 주소를 이용한 호스트 이름 찾기 프로그램

import socket

hostname, aliases, addresses = socket.gethostbyaddr('66.33.211.242')

print('Hostname :', hostname)
print('Aliases  :', aliases)
print('Addresses:', addresses)