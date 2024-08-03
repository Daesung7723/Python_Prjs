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

async def main():
    svr = '127.0.0.1'
    port = 2500

    #클라이언트가 연결되면 handle_echo callback이 실행되고, reader/writer가 전달된다
    coro = await asyncio.start_server(handle_echo, svr, port) # Py 3.8부터 loop는 사용되지 않음
    
    async with coro:
        await coro.serve_forever()

asyncio.run(main())