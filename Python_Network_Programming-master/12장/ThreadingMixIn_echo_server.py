#ThreadingMixIn + TCPServer 클래스를 이용한 멀티 클라이언트 에코 서버
import socketserver
import threading

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self): #요청 처리 메소드
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        while True:
            data = self.rfile.readline() #데이터 수신
            if not data:
                break
            print(data.decode())
            self.wfile.write(data) #데이터 송신
        print(f'Closed: {client}')

with socketserver.ThreadingTCPServer(('', 2500), RequestHandler) as server:
    print(f'The echo server is running...')
    server.serve_forever() #요청을 처리한다