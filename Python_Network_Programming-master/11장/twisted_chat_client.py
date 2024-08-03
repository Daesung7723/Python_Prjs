# Thread와 twisted를 사용한 채팅 클라이언트
# 메시지 송수신이 독립적으로 수행된다

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

class ChatClient(Protocol):
    def __init__(self):
        reactor.callInThread(self.sendMessage) #메시지 송신 무한루프를 스레드로 실행
        
    def connectionMade(self):
        print("Connected to chat server")
    
    def dataReceived(self, data):
        data = data.decode()
        print(data)
            
    def sendMessage(self):
        while True:
            self.transport.write(input().encode())
        

class ChatClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ChatClient()
    
    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason.getErrorMessage()}")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()

if __name__ == '__main__':
    host = "localhost"
    port = 2500
    
    endpoint = TCP4ClientEndpoint(reactor, host, port)
    endpoint.connect(ChatClientFactory())
    reactor.run()
