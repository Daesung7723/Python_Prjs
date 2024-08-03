#프레임 생성과 파싱 프로그램
import socket
import capsule #프레임 구성 사용자 모듈

SIZE = 5 #페이로드 크기
sock = socket.socket() #TCP 소켓
sock.setblocking(True) #블록킹 모드
sock.settimeout(0.1) #타임아웃=0.1
sock.connect(('localhost', 2500)) #서버 연결

#header 구성
header = {"START": 0x05, "ADDR": 1, "NO": 1, "LENGTH": SIZE}
header_size = 11 #시작문자:1, 주소: 2, 순서번호: 4, 길이: 4

frame_seq="" #전송 프레임
msg = "hello world"
print("전송 메시지: ", msg)

for i in range(0, len(msg), SIZE):
    start = i
    frame_seq += capsule.frame(header["START"], header["ADDR"],
                               header["NO"], msg[start:start+SIZE])
    start += SIZE
    header["NO"] += 1

sock.send(frame_seq.encode()) #복수의 프레임을 구성하여 전송

r_msg = '' #수신 메시지
seq_num = 1
while True:
    try:
        if sock.recv(1).decode() == chr(0x05): #프레임 시작?
            p_msg = sock.recv(header_size-1).decode() #header
            
            if int(p_msg[2:6]) == seq_num: #순서번호 확인
                payload_len = int(p_msg[-4:]) #payload 길이
                segment = sock.recv(payload_len).decode()
                print("수신 프레임 ", segment)
                r_msg = r_msg + segment #메시지 구성
                seq_num += 1
            else:
                print("재전송 요청")
    except:
        break

print("복원 메시지: ",r_msg)
sock.close()