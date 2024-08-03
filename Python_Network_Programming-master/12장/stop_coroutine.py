# 코루틴 중지 프로그램

import asyncio

async def say(what, delay):
    await asyncio.sleep(delay)
    print(what)

async def stop_after(loop, delay):
    await asyncio.sleep(delay)
    loop.stop()

try:
    loop = asyncio.get_running_loop()
except:
    loop = asyncio.new_event_loop()

loop.create_task(say('first message', 2))
loop.create_task(say('second message', 1))
loop.create_task(say('third message', 4))
loop.create_task(stop_after(loop, 3))

loop.run_forever()
loop.close()