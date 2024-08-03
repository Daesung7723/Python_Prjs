# asyncio.wait(coros)를 이용한 복수 코루틴 실행 프로그램
# Python 3.7+
 
import asyncio
import random
import time
 
async def say(msg, delay=1):
    print(f'{msg!r} will be displayed in {delay} seconds')
    await asyncio.sleep(delay)
    return msg.upper()
 
async def main():
    messages = 'hello world apple banana cherry'.split()
    cos = [say(m, random.randrange(1,5)) for m in messages]
    
    #코루틴을 스케줄링하고 완료된 태스크 집합과 미완료 태스크 집합을 반환받는다
    #await를 호출하여 코루틴의 실행 결과를 반환받는다
    start_time = time.time() #시작 시각
    done, pending = await asyncio.wait(cos) #코루틴을 한 번에 스케줄링
    
    for task in done: #완료된 태스크의 깂을 반환받는다
        print(await task)
    print(f'{time.time() - start_time}') #총 소요시간
        
asyncio.run(main())
