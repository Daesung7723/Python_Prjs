#create_datagram_endpoint()를 이용한 이벤트 방식 서버 프로그램

import asyncio

#이벤트 콜백을 정의하는 프로토콜 클래스
class EchoServerProtocol:
    
    #연결이 성공하면 호출되는 콜백
    def connection_made(self, transport):
        self.transport = transport #소켓

    #데이터를 수신하면 호출되는 콜백
    #data(수신된 데이터)와 addr(상대방 주소)가 이벤트 루프에서 전달된다
    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr) #데이터 송신

async def main():
    print("Starting UDP server")

    # 현재의 이벤트 루프를 가져온다.
    loop = asyncio.get_running_loop()

    #UDP 채널을 생성하고 protocol 객체를 콜백으로 지정한다
    #(transport, protocol) 객체가 반환된다. transport는 소켓 객체이고,
    #protocol은 소켓 이벤트를 위한 callback이 정의된 클래스 객체이다
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(), #protocol 객체
        local_addr=('127.0.0.1', 2500))
    
    try:
        await asyncio.sleep(3600)  # 1시간 동안 서비스
    finally:
        transport.close()
    
asyncio.run(main())