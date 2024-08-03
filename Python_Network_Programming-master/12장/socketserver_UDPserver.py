#socketserver 모듈을 이용한 UDP 에코 서버 프로그램

import socketserver

class UDPHandler(socketserver.BaseRequestHandler):

    #데이터가 수신되면 한번 실행
    def handle(self):
        
        #data = self.request[0], socket = self.request[1]
        #address = self.client_address
        data = self.request[0].strip() #수신 데이터
        socket = self.request[1] #연결 소켓
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address) #재전송

if __name__ == "__main__":
    HOST, PORT = "", 2500
    
    #UDP 소켓을 생성하고 실행
    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()