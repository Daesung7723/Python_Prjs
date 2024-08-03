# 여러 개의 코루틴을 동시에 스케줄링하고 완료된 순서대로 결과를 반환
 
import asyncio
import random
 
async def say(msg, delay=1):
    print(f'{msg!r} will be displayed in {delay} seconds')
    await asyncio.sleep(delay)
    return msg.upper()
 
async def main():
    messages = 'pear peach apple banana cherry'.split()
    
    #코루틴 리스트
    coros = [say(m, random.randrange(1,5)) for m in messages]
    
    #코루틴을 스케줄링하고 완료되는 코루틴을 차례대로 반환
    for coro in asyncio.as_completed(coros):
        #coro = 완료된 코루틴
        #await로 완료된 코루틴의 결과를 반환받는다
        msg = await coro
        print(msg)

asyncio.run(main())
