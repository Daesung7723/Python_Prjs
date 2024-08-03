# start_server()를 이용하여 다수의 클라이언트를 반복 서비스하는 에코 서버 프로그램

import asyncio

#클라이언트와 연결되면 실행되는 코루틴
#(reader, writer)는 이벤트 루프가 전달
async def handle_echo(reader, writer):
    
    while True: #연결된 클라이언트를 계속 서비스한다
        data = await reader.read(100) #비블록킹으로 동작하므로 무조건 리턴됨
        
        if data: #수신 데이타가 있으면
            message = data.decode()
            addr = writer.get_extra_info('peername') #상대방 주소
            print(f"Received {message!r} from {addr!r}")
            
            print(f"Send: {message!r}")
            writer.write(data) #메시지 송신
            await writer.drain() #모두 송신될 때까지 대기

async def main():
    #서버 객체를 생성하여 실행 예약
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 2500)
    print(len(server.sockets))
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    
    async with server:
        await server.serve_forever() #서버 무한 반복
        
asyncio.run(main())