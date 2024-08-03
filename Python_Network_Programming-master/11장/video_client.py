# Video client(수신)
import socket,cv2, pickle,struct, sys

# 소켓 생성
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST_IP = 'localhost' # 서버 IP 주소
TCP_PORT = 9000

client_socket.connect((HOST_IP,TCP_PORT)) # 서버와 연결
print("Connected")
data = b""
payload_size = struct.calcsize("Q") # 길이 정보를 unsigned 8bytes로 표시

while True:
    while len(data) < payload_size: # 수신 프레임은 길이 영역(8바이트)보다 커야 한다
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break # 연결 종료?
        data += packet
    packed_msg_size = data[:payload_size] # 프레임 길이 추출
    data = data[payload_size:] # 프레임 추출
    msg_size = struct.unpack("Q",packed_msg_size)[0] # 프레임 길이를 파이썬 자료형으로 변환
    
    while len(data) < msg_size: # 길이 만큼의 frame을 수신한다
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size] # 한 프레임 크기를 잘라낸다
    data  = data[msg_size:] # 다음 프레임(next frame)
    
    # 동영상 프레임 표시
    frame = pickle.loads(frame_data) # 바이트 스트림을 프레임으로 변환
    cv2.imshow("Client Video",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        cv2.destroyAllWindows()
        break

client_socket.close()
sys.exit()