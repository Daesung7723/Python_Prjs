import socket as so
import struct
from random import randint

sock = so.socket()
addr = ('', 502) #Modbus TCP는 502 포트 사용
sock.bind(addr)
sock.listen()
client, adr = sock.accept()

while True:
    # 수신(요청) 패킷 분해
    packet = client.recv(1024) # master packet 수신
    print("\n요청 패킷")
    for e in packet:
        print("{:02x}".format(e), end=' ')
    
    Tr, Pr, Le, ID, Code, Addr, Reg = struct.unpack(">HHHBBHH", packet)
    print("\nTransaction ID=", Tr)
    print("Protocol ID=", Pr)
    print("Length=", Le)
    print("Unit ID=", ID)
    print("Function Code=", Code)
    print("Starting Address=", Addr)
    
    
    #Function Code=3에 대한 응답 패킷 구성
    if Code == 0x03: # master에게 데이터 전송
        print("Number of registers=", Reg)
        #임의의 데이터 준비
        data = bytes()
        for i in range(Reg):
            data = data + struct.pack(">H", randint(0,255)) # 2바이트씩
        Le = len(data)+3 # # data 길이 + Unit_ID(1) + Function Code(1) + 바이트수(1)
        # 응답 패킷 구성
        resp = struct.pack(">HHHBBB", Tr, Pr, Le, ID, Code, Reg*2) + data
    
    #Function Code=6에 대한 응답 패킷 구성(응답 패킷 = 요청 패킷)
    elif Code == 0x06: # master 데이터 저장
        print("Register value=", Reg)
        resp = packet
    
    # 응답 전송
    client.send(resp)
    print("응답 패킷")
    for e in resp:
        print("{:02x}".format(e), end=' ')
    print()