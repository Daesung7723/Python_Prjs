# open_connection()을 이용한 TCP 클라이언트 프로그램

import asyncio

async def tcp_echo_client(message):
    #소켓을 생성하고 연결하는 코루틴
    reader, writer = await asyncio.open_connection(
        'localhost', 2500)

    #데이터 송신
    print('송신: {!r}'.format(message))
    writer.write(message.encode()) #코루틴이 아니므로 동기식 전송

    data = await reader.read(100) #메시지 수신(코루틴)
    print('수신: {!r}'.format(data.decode()))
    
    print('연결 종료')
    writer.close() #송신 연결 종료

async def main():
    message = 'Hello Server!'
    await tcp_echo_client(message)

asyncio.run(main())