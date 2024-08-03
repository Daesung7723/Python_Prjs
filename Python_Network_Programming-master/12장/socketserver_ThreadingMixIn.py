#ThreadingMixIn을 이용한 비블록킹 소켓 TCP 에코 서버 프로그램

import socket
import threading
import socketserver

#소켓 요청 처리 클래스
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'utf-8') #self.request = 소켓
        cur_thread = threading.current_thread() #실행 스레드
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response) #서버 응답 전송

#서버 객체 생성 클래스
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

#클라이언트 함수
def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'utf-8'))
        response = str(sock.recv(1024), 'utf-8')
        print("수신: {}".format(response))

if __name__ == "__main__":
    
    host, port = "localhost", 2500
    
    #서버 객체를 생성하고 요청 처리 클래스 지정
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    
    #서버를 위한 스레드 생성과 실행
    ip, port = server.server_address #서버 주소와 포트
    server_thread = threading.Thread(target=server.serve_forever) #스레드 생성
    server_thread.daemon = True
    server_thread.start()
    print(f"{server_thread.name} 스레드에서 서버 실행")
    
    #클라이언트 호출
    client(ip, port, "안녕하세요 1")
    client(ip, port, "안녕하세요 2")
    client(ip, port, "안녕하세요 3")

    server.shutdown() #서버 종료