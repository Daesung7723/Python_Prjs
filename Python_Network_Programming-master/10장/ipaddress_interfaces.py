# 인터페이스 주소 속성 조사 프로그램

import ipaddress


ADDRESSES = [
    '10.9.0.6/24',
    'fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64',
]


for ip in ADDRESSES:
    iface = ipaddress.ip_interface(ip) #인터페이스 주소
    print('{!r}'.format(iface))
    print('network:\n  ', iface.network) #네트워크 주소
    print('ip:\n  ', iface.ip) #호스트 주소
    print('IP with prefixlen:\n  ', iface.with_prefixlen) #CIDR 표기
    print('netmask:\n  ', iface.with_netmask) #넷마스크
    print('hostmask:\n  ', iface.with_hostmask) #호스트 마스크
    print()
