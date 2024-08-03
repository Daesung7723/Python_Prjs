#threading class를 이용한 TCP 에코 서버 프로그램

import socket, threading

#threading.Thread의 서브 클래스
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self) #부모 클래스 초기화 함수 실행
        self.csocket = clientsocket #인스턴수 변수 정의
        self.addr = clientAddress
        print ("New socket added: ", self.addr)

    def run(self): #자동 실행
        print ("Connection from : ", self.addr)

        msg = ''
        while True:
            data = self.csocket.recv(2048) #데이터 수신
            msg = data.decode()
            
            if msg=='quit': #quit가 수신되면 종료
              break
            
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8')) #에코
            
        print ("Client at ", self.addr , " disconnected...")

LOCALHOST = ""
PORT = 2500

#서버 소켓 생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
server.listen(1)

while True: #클라이언트 마다 하나의 스레드가 배정된다
    
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()