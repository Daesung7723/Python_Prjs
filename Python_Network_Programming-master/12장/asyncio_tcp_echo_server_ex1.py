# start_server()를 이용한 비동기 에코 서버 프로그램

import asyncio

async def handle_echo(reader, writer):
    while True: #연속 에코 서비스
        read_task = asyncio.create_task(recv_message(reader))
        msg = await read_task
        writer.write(msg)
        
async def recv_message(reader):
    r_msg = await reader.read(100)
    print('Received: ',r_msg)
    return r_msg

loop = asyncio.get_event_loop()
#client가 연결되면 handle_echo callback이 실행된다
coro = asyncio.start_server(handle_echo, '', 2500, loop=loop) 

task = loop.create_task(coro)
loop.run_forever()
