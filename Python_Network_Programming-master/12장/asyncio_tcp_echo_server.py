# start_server()를 이용한 TCP 에코 서버 프로그램

import asyncio

#데이터 수신 처리 코루틴
#클라이언트와 연결되면 한 번만 실행됨
async def handle_echo(reader, writer): 
    data = await reader.read(100) #데이터 수신
    message = data.decode()
    addr = writer.get_extra_info('peername') #상대방 주소
    print(f"{addr!r}에서 {message!r}를 수신함")
        
    print(f"송신: {message!r}")
    writer.write(data)
    await writer.drain()
    print("클라이언트 소켓 닫음")
    writer.close()

svr = '127.0.0.1'
port = 2500
try:
    loop = asyncio.get_running_loop()
except:
    loop = asyncio.new_event_loop()

#클라이언트가 연결되면 handle_echo callback이 실행된다
coro = asyncio.start_server(handle_echo, svr, port, loop=loop) 
server = loop.run_until_complete(coro) #코루틴이 완료될 때까지 기다린다

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever() #계속 연결 서비스
except KeyboardInterrupt:
    pass

#서버 객체를 닫는다
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()