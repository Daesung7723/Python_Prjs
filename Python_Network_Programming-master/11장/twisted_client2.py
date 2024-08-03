from twisted.internet import reactor, protocol, stdio
from twisted.protocols.basic import LineReceiver


class ChatClient(LineReceiver):
    def connectionMade(self):
        self.sendLine(b"CONNECT")
        print("Connected to chat server")
        self.factory.client = self
    
    def lineReceived(self, line):
        message = line.decode().strip()
        if message == "NICKNAME":
            self.sendLine(input("Enter your nickname: ").encode())
        elif message == "NICKNAME ACCEPTED":
            print(f"Nickname '{self.factory.nickname}' has been accepted")
        else:
            print(message)
    
    def sendMessage(self, message):
        self.sendLine(f"MESSAGE {message}".encode())


class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClient
    
    def __init__(self, nickname):
        self.nickname = nickname
        self.client = None
    
    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        return p
    
    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason.getErrorMessage()}")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()


class StdioWrapper(LineReceiver):
    delimiter = b'\n'
    
    def __init__(self, protocol):
        self.protocol = protocol
    
    def connectionMade(self):
        self.transport.write(b"> ")
    
    def lineReceived(self, line):
        message = line.decode().strip()
        if message:
            self.protocol.sendMessage(message)
        msg = input("message:")
        self.transport.write(msg.encode())
        #self.transport.write(b"> ")


if __name__ == '__main__':
    host = "localhost"
    port = 2500
    
    nickname = input("Enter your nickname: ")
    factory = ChatClientFactory(nickname)
    
    reactor.connectTCP(host, port, factory)
    
    stdio.StandardIO(StdioWrapper(factory.client))
    
    reactor.run()
