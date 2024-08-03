# Video server
# Capturing a video stream from webcam and sending it to client

import socket, cv2, pickle, struct, imutils, sys

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
TCP_PORT = 9000
server_addr = ('', TCP_PORT)

# 주소와 포트번호 바인드
server_socket.bind(server_addr)

# 접속 대기
server_socket.listen(5)
print("서버 접속 대기:", server_addr)

# 클라이언트 연결
while True:
    client_socket, addr = server_socket.accept()
    print(addr, '와 연결됨')
    mode = int(input("WebCam(1) or MP4(2): "))
    
    if client_socket:
        if mode == 1:
            # WebCAM 사용
            vid = cv2.VideoCapture(0) # WebCam
        else:
            # 동영상 플레이
            vid = cv2.VideoCapture("동양미래대학교.mp4") # MP4
            if vid.isOpened(): print('width: {}, height : {}'.format(vid.get(3), vid.get(4)))

        while (vid.isOpened()):
            img, frame = vid.read() # 프레임 획득
            if not img:
                break
            frame = imutils.resize(frame, width=1024) # 프레임 크기 조절
            frame_bytes = pickle.dumps(frame) # 프레임을 바이트 스트림으로 변환
            message = struct.pack("Q", len(frame_bytes)) + frame_bytes # frame 길이(unsigned 8bytes) + frame
            try:
                client_socket.sendall(message) # 길이 + 프레임 전송
                
            except:
                print("연결이 종료됨")
                client_socket.close()
                break

            cv2.imshow('Server Video', frame) # 전송 영상 표시
            key = cv2.waitKey(1) & 0xFF # 'q' 입력 대기
            if key == ord('q'):
                client_socket.close()
                break
                
        vid.release()
        cv2.destroyAllWindows() # 화면을 닫는다
        sys.exit() # 명령창을 닫는다
