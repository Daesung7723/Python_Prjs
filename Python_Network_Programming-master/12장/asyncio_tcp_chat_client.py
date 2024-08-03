# open_connection()을 이용한 TCP 채팅 클라이언트 프로그램

import asyncio, time

async def tcp_echo_client(message, loop):
    
    #서버와 연결하고 reader, writer를 반환 받는다 
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 2500, loop=loop)
    
    #태스크를 생성하고 실행한다
    read_task = asyncio.create_task(recv_message(reader))
    write_task = asyncio.create_task(send_message(writer))


#메시지 수신 코루틴
async def recv_message(reader):
    while True:
        r_msg = await reader.read(100)
        print('<-', r_msg.decode())


#메시지 송신 코루틴
async def send_message(writer):
    while True:
        s_msg = await loop.run_in_executor(None, input, '') #input() 비동기 실행
        writer.write((id+s_msg).encode())


message = 'Hello World'
id = input('이름: ')
id = '['+id+'] '

#이벤트 루프를 가져온다
loop = asyncio.get_event_loop()

#이벤트 루프에서 코루틴 실행
loop.run_until_complete(tcp_echo_client(message, loop))
loop.run_forever()            