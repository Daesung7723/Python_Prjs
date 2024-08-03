#create_datagram_endpoint()를 이용한 이벤트 방식 클라이언트 프로그램

import asyncio

#이벤트 콜백을 정의하는 프로토콜 클래스
class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()
        
    #연결이 성공하면 호출되는 콜백
    def connection_made(self, transport):
        self.transport = transport #소켓
        print('Send:', self.message)
        self.transport.sendto(self.message.encode()) #데이터 전송

    #데이터를 수신하면 호출되는 콜백
    #data(수신된 데이터)와 addr(상대방 주소)가 이벤트 루프에서 전달된다
    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    #오류 발생 시 호출되는 콜백
    def error_received(self, exc):
        print('Error received:', exc)

    #연결이 종료되면 호출되는 콜백
    def connection_lost(self, exc):
        print("Connection closed")
        
        #연결이 종료되면 퓨처를 실행 완료로 설정하고 True 반환
        self.on_con_lost.set_result(True)


async def main():
    # 저수준 API를 사용하기 위해 현재 이벤트 루프를 가져온다
    loop = asyncio.get_running_loop()

    message = "Hello World!" #전송 메시지
    
    #UDP 채널을 생성하고 protocol 객체를 콜백으로 지정한다
    #(transport, protocol) 객체가 반환된다. transport는 소켓 객체이고,
    #protocol은 소켓 이벤트를 위한 callback이 정의된 클래스 객체이다
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, loop),
        remote_addr=('127.0.0.1', 2500))

    try:
        await protocol.on_con_lost #퓨처 종료 대기
    finally:
        transport.close() #소켓을 닫는다

asyncio.run(main())