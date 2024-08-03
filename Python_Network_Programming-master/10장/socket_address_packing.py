# 문자열 주소와 2진수 주소의 상호 변환 프로그램

import binascii
import socket

for string_address in ['203.249.39.46','127.0.0.1']:
    packed =socket.inet_aton (string_address )#문자열 주소를 2진수로 변환
    print ('Original:',string_address )
    print ('Packed  :',binascii.hexlify (packed )) #2진수를 16진수로 표현
    print ('Unpacked:',socket.inet_ntoa (packed )) #2진수 주소를 문자열로 변환
    print ()
