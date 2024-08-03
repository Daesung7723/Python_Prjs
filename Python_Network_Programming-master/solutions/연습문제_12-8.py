#socketserver 모듈을 이용한 UDP 채팅 서버 프로그램

import socketserver

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #data = self.request[0], socket = self.request[1]
        #address = self.client_address
        
        #데이터가 수신되면 한번 실행
        print("<- ", end ='')
        print(self.request[0].decode())
        
        while True:
            resp = input("-> ")
            self.request[1].sendto(resp.encode(), self.client_address)

            data, self.client_address = self.request[1].recvfrom(1024) #수신 데이터
            print("<- ", end ='')
            print(data.decode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 2500
    
    #UDP 소켓을 생성하고 실행
    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()