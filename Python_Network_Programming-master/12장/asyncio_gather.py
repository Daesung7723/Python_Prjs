# asyncio.gather(*coros)를 이용한 동시 실행 프로그램
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
    
    #코루틴 리스트에 있는 코루틴 객체가 모두 종료되어야 반환됨
    #따라서 코루틴을 호출할 때 가장 지연 시간이 긴 코루틴이 종료되어야 반환됨
    start_time = time.time() #시작 시각
    results = await asyncio.gather(*cos)
    
    print(results)
    print(f'{time.time() - start_time}') #총 소요시간
        
asyncio.run(main())
