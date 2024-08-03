# 태스크를 생성하여 복수의 코루틴을 실행하는 프로그램

import asyncio
import time

async def say(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def main():
    task1 = asyncio.create_task(say(2, 'Hello'))
    task2 = asyncio.create_task(say(1, 'World'))
    
    print(f"started at {time.strftime('%X')}")

    await task1 #task1 완료 대기
    await task2 #task2 완료 대기
    
    print(f"finished at {time.strftime('%X')}")
 
asyncio.run(main())