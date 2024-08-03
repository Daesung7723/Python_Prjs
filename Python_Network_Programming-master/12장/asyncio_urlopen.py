from time import time
from urllib.request import Request, urlopen
import asyncio
 
urls = ['https://www.google.co.kr/search?q=' + i
        for i in ['apple', 'pear', 'grape', 'pineapple', 'orange', 'strawberry']]
 
async def fetch(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    # UA가 없으면 403 에러 발생
    response = await loop.run_in_executor(None, urlopen, request)    # run_in_executor 사용
    page = await loop.run_in_executor(None, response.read)           # run in executor 사용
    return len(page)
 
async def main():
    # 태스크 객체를 리스트로 만듦
    # ensure_future()의 인수가 코루틴이면 태스크 객체가 반환됨
    futures = [asyncio.ensure_future(fetch(url)) for url in urls]
    # 결과를 한꺼번에 가져옴
    result = await asyncio.gather(*futures)
    print(result)
 
begin = time()
try:
    loop = asyncio.get_running_loop()          # 이벤트 루프를 얻음
except:
    loop = asyncio.new_event_loop()
loop.run_until_complete(main())          # main이 끝날 때까지 기다림
loop.close()                             # 이벤트 루프를 닫음
end = time()
print('실행 시간: {0:.3f}초'.format(end - begin))