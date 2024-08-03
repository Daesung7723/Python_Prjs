# socketserver 모듈을 이용한 echo 서버
import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self): #연결 설정
        print("Connected")
        
    def handle(self): #데이터 수신
        while True: #연결을 유지하려면 무한 루프 실행
            # self.request = client socket
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    #self.finish()
                    return
            except:
                self.finish()
                return
            print(("{} wrote:".format(self.client_address[0])))
            print((self.data))
            

            # 수신 메시지 전송
            self.request.sendall(self.data.upper())
    
    def finish(self): #연결 해제
        print("Disconnected")
        self.request.close()
            
if __name__ == "__main__":
    HOST, PORT = "", 2500
    # 서버 객체 생성
    server = socketserver.TCPServer((HOST, PORT), TCPHandler, bind_and_activate=True)

    # 서버 실행
    server.serve_forever()
