import socket as so
import struct, time

sock = so.socket()
addr = ('localhost', 502) # Modbus TCP는 502 포트 사용
sock.connect(addr) # Modbus Slave 접속
while True:
    Code = int(input("Function Code:"))
    if Code < 1 or Code > 6:
        print("A Wrong Function Code")
        continue
    else:
        break
Tr = 0 # Transaction ID
Pr = 0 # Protocol ID
Le = 6 # Length
ID = 1 # Unit ID
Addr = 0 # Satrting Address
if Code <= 0x04: #Read
    Data = 10 # 읽을 레지스터 수
elif 0x05 <= Code <= 0x06: #Write
    Data = 0xff00 # 레즈스터에 써 넣을 값
    
# 요청 패킷 구성
MBAP_Header =  struct.pack(">HHB", Pr, Le, ID) # MBAP Header
PDU =  struct.pack(">BHH", Code, Addr, Data) # PDU
print("\nTransaction ID=", Tr)
print("Protocol ID=", Pr)
print("Length=", Le)
print("Unit ID=", ID)
print("Function Code=", Code)
print("Starting Address=", Addr)

if Code <= 0x04: #Read
    print("Number of registers=", Data) # 읽을 레지스터 수
elif 0x05 <= Code <= 0x06: #Write
    print("Register value=", Data) # 레즈스터에 써 넣을 값

# 요청 패킷
packet = MBAP_Header + PDU
    
while True:
    Tran_ID = struct.pack(">H", Tr) # Transaction ID 추기
    Spacket = Tran_ID + packet
    sock.send(Spacket)
    print("\nReqeust Packet")
    for e in Spacket:
        print('{:02x}'.format(e), end=' ')
        
    resp = sock.recv(1024) #응답 수신
    print("\nResponse Packet")
    for e in resp:
        print('{:02x}'.format(e), end=' ')
    Tr += 1 #next transaction
    time.sleep(0.5)