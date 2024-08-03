# 일반 함수를 비동기로 실행하는 프로그램

import asyncio as aio

async def coro1(): #3초 마다 숫자 출력
    i = 1
    while True:
        print(i)
        i = i + 1
        await aio.sleep(3)
        
async def coro2(loop): #키보드 입력을 다시 출력
    while True:
        msg = await loop.run_in_executor(None, input, ': ')
        print('->',msg)
    
async def main():
    try:
        loop = aio.get_running_loop() #코루틴에서 이벤트 루프를 얻을 때
    except:
        loop = aio.new_event_loop()
    task1 = loop.create_task(coro1())
    task2 = loop.create_task(coro2(loop))
    
    await task1
    await task2

aio.run(main())