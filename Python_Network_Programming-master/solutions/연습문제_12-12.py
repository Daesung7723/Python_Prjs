# 일반 함수를 비동기로 실행하는 프로그램

import asyncio as aio
import time

async def coro1():
    # 1초 마다 숫자 출력
    i = 1
    while True:
        print(i)
        i = i + 1
        await aio.sleep(1)
        
async def coro2(loop):
    # 키보드 입력을 다시 출력
    while True:
        msg = await loop.run_in_executor(None, input, ': ')
        print('->',msg)
    
async def main():
    loop = aio.get_running_loop() #코루틴에서 이벤트 루프를 얻을 때
    coros = [coro1(), coro2(loop)]
    await aio.gather(*coros)


aio.run(main())