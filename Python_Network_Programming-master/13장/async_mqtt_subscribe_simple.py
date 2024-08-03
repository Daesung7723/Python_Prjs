# asyncio를 이용한 간단한 mqtt 메시지 구독 프로그램

import paho.mqtt.subscribe as subscribe
import asyncio

broker = "test.mosquitto.org"
async def sub_msg(topic):
    try:
        loop = asyncio.get_running_loop()
    except:
        loop = asyncio.new_event_loop()
    m = await loop.run_in_executor(None, subscribe.simple,topic, 0, 1, False, broker)#매개변수는 순서대로 나열
    print("Topic= ",m.topic, ", Message= ", m.payload.decode())

    return "OK"
    
async def main():
    task1 = asyncio.create_task(sub_msg("mqtt/test"))
    task2 = asyncio.create_task(sub_msg("TestTopic"))

    tasks = [task1, task2]
       
    for done_task in asyncio.as_completed(tasks): #완료된 태스크 조사
        result = await done_task #완료된 태스크 반환값 처리
        print(result)

asyncio.run(main())
