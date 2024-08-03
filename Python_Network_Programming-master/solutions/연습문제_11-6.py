#UDP 소켓을 이용한 파일 송수신 프로그램
#수신을 먼저 실행하고 송신한다

import socket, time, sys, os

ACK = bytes([0x06]) # ACK
BUFSIZE = 8096*8

def Receiver():
    sock.bind(addr)
    
    print("수신 대기 중...")
    fn, client = sock.recvfrom(BUFSIZE) #파일 이름 수신
    fn = os.path.basename(fn.decode()) # 기본 파일이름 추출
    print("파일 이름: ", fn)
    
    sock.sendto(ACK, client) #응답
    print("응답 전송")
    
    path = 'c:/Temp/' # 파일 저장 경로
    with open(path+fn, "wb") as fp:
        print("파일 수신 중...")
        while True:
            data, _ = sock.recvfrom(BUFSIZE)
            if not data: #수신 완료
                break
            fp.write(data) #수신 데이터를 파일에 저장
            sock.sendto(ACK, client)
            
    print("Saved in "+ path + fn)
    print("수신 완료")


def Sender():
    file_name = input("전송 파일: ")
    sock.sendto(file_name.encode(), addr) #파일 이름 전송
    resp, client = sock.recvfrom(BUFSIZE) #응답 수신
    
    if resp == ACK: # ACK 수신
        fp = open(file_name, "rb")
        data = fp.read(BUFSIZE)
        sock.sendto(data, client)
        print("송신 중...")
    
        while True:
            resp, _ = sock.recvfrom(BUFSIZE) #응답 수신
            if resp == ACK:
                data = fp.read(BUFSIZE)
                if data:
                    sock.sendto(data, client)
                else:
                    break
            
        sock.sendto(data, client) #송신 완료를 위해 빈 데이터 전송
        fp.close()
        print("전송 완료")
    else:
        print("수신 응답 오류")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('localhost', 2500)
    try:
        role = sys.argv[1] #송신(s) 또는 수신(r)
        if role == 's':
            Sender()
        elif role == 'r':
            Receiver()
        else:
            print("s(송신) 또는 r(수신)을 지정하세요")
    except:
        print("송수신 오류")