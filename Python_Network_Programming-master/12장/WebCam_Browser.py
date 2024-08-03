import logging
import socketserver, cv2, imutils, threading
from threading import Condition
from http import server

#HTML
PAGE="""\
<html>
<head>
<title>WebCam streaming</title>
</head>
<body>
<h2>WebCam Streaming using ThreadingMixIn and http.server</h2>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

def record():
    global vid, output

    # WebCam 영상을 jpg로 변환하여 버퍼에 저장
    while vid.isOpened():
        #이미지를 읽어온다
        img, frame = vid.read() #img: 결과(T/F), frame: 이미지
        #이미지 크기 조정
        frame = imutils.resize(frame, width=640) # numpy array type
        #이미지를 jpg 포맷으로 압축한다
        _, jpg = cv2.imencode(".jpg", frame) #압축 결과(_)는 사용하지 않는다
        #jpg로 압축된 이미지를 버퍼에 저장한다
        output.write(jpg)


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.condition = Condition() # 조건변수 설정. thread 사이의 동기화를 위해 사용

    def write(self, buf):
        # 동기가 맞으면 압축 영상을 frame에 저장
        with self.condition:
            self.frame = buf 
            self.condition.notify_all() # 조건변수 충족 통지
        

#웹 서버 핸들러 클래스
class StreamingHandler(server.BaseHTTPRequestHandler):
    # GET Server
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content) # Web browser에 응답 전송
        
        elif self.path == '/stream.mjpg': # <img src="stream.mjpg" width="640" height="480" />
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait() # frame이 준비될 때까지 대기
                        frame = output.frame # frame을 가져온다
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame) # web browser에게 frame 전송
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True # socketserver 속성. 주소 재사용
    daemon_threads = True # ThreadingMixIn 속성. 서브 스레드가 종료되면 즉시 종료


vid = cv2.VideoCapture(0)
output = StreamingOutput()

# WebCam 영상을 연속적으로 버퍼로 전송하는 스레드
v_th = threading.Thread(target=record, args=())
v_th.daemon = True
v_th.start()

# 다중 클라이언트 지원 서버 실행
try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler) # server 객체를 생성하고 thread로 실행
    server.serve_forever()
finally:
    vid.release()
