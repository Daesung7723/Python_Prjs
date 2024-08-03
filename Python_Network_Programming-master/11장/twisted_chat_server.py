from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class ChatServer(Protocol):
    def __init__(self, users):
        self.users = users
        
    def connectionMade(self):
        print("New connection")
        self.users.append(self) #연결된 크라이언트를 목록에 추가
        self.transport.write("Hello from server".encode())
        
    def dataReceived(self, data):
        for user in self.users:
            if user != self: # 메시지 송신자 제외
                user.transport.write(data)
            
            
class ChatServerFactory(ServerFactory):
    def __init__(self):
        self.users = [] #접속된 클라이언트 목록 저장
        
    def buildProtocol(self,addr):
        return ChatServer(self.users)
    
if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2500)
    endpoint.listen(ChatServerFactory())
    reactor.run()
    
        