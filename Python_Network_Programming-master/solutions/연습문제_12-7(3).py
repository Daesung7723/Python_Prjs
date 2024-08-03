#TCP 프로세싱 서버 프로그램
#숫자를 받아 영어를 송신한다

import socketserver

#숫자에 대한 영어 사전
table = {'1':'one', '2': 'two', '3': 'three', '4': 'four',\
'5':'five', '6': 'six', '7': 'seven', '8': 'eight',\
'9': 'nine', '10': 'ten'}

class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self): #연결 설정
        print("Connected")
        
    def handle(self): #데이터 수신
        while True: #연결을 유지하려면 무한 루프 실행
            # self.request = client socket
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    print("Connection closed")
                    return
            except:
                print("No connection")
                return
            
            try:
                print(self.data.decode())
                resp = table[self.data.decode()] #데이터를 key로 사용하여 value를 가져온다
            except:
                self.request.send('Try again'.encode()) #오류가 있을 때
            else:
                self.request.send(resp.encode()) # vlaue 전송
                    
    def finish(self): #연결 해제
        print("Disconnected")
        self.request.close()
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 2500
    # 서버 객체 생성
    server = socketserver.TCPServer((HOST, PORT), TCPHandler, bind_and_activate=True)

    # 서버 실행
    server.serve_forever()
