# IPv6 주소 표현 변환 프로그램

import binascii
import socket

string_address ='2002:ac10:10a:1234:21e:52ff:fe74:40e'

#문자열을 압축 바이너리로 변환
packed =socket.inet_pton(socket.AF_INET6 ,string_address ) 

print ('Original:',string_address )
print ('Packed  :',binascii.hexlify(packed ))
#압축 바이너리를 문자열로 변환
print ('Unpacked:',socket.inet_ntop(socket.AF_INET6 ,packed ))