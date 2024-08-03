import socket
import cv2, imutils

UDP_IP = 'localhost'
UDP_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# WebCam 객체 생성
cap = cv2.VideoCapture(0)
fSize = 46080
#if cap.isOpened():
#    print("width: {}, height: {}".format(cap.get(3), cap.get(4)))

while cap.isOpened():
    # Video frame을 읽는다. 성공하면 ret = True, 실패하면 ret = False
    ret, frame = cap.read()
    cv2.imshow("Client Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sock.close()
        cap.release()
        break

    # frame을 1차원으로 변환
    #one_d_frame = frame.flatten()
    #send_frame = one_d_frame.tobytes()
    send_frame = umtils.resize(frame, width=640)
    send+frame = pickle.dumps(send_frame)

    for i in range(20):
        # 프레임을 46080 바이트씩 전송. 프레임 번호를 헤더로 사용
        #sock.sendto(bytes([i]) + send_frame[i*fSize:(i+1)*fSize], (UDP_IP, UDP_PORT))
        sock.sendto(bytes([i]) + send_frame[i*fSize:(i+1)*fSize], (UDP_IP, UDP_PORT))
