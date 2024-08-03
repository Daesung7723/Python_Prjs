# socketserver 모듈을 이용한 echo 서버
import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self): #데이터 수신
        self.data = self.request.recv(1024).strip()
        print(("{} wrote:".format(self.client_address[0])))
        print((self.data))
            
        # 수신 메시지 전송
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 2500
    # 서버 객체 생성
    server = socketserver.TCPServer((HOST, PORT), TCPHandler, bind_and_activate=True)

    # 연결 대기 동작 계속
    print("waiting")
    server.serve_forever()
