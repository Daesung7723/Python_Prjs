# ipaddress 모듈의 속성 조사 프로그램

import binascii
import ipaddress

ADDRESSES =[
    '192.168.0.5',
    '2001:0:9d38:6abd:480:f1f:3f57:fffb',
]

for ipaddr in ADDRESSES :
    addr =ipaddress.ip_address(ipaddr)
    print(f'IP address: {addr!r}') #IP 주소
    print('IP version:',addr.version) #버전
    print('Packed addr:',binascii.hexlify(addr.packed)) #압축 바이너리 주소
    print('Integer addr:',int(addr)) #정수형 주소
    print('Is private?:',addr.is_private) #사설망 조사
    print()