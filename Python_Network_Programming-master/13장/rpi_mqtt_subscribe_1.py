# 라즈베리 파이가 발행하는 메시지를 구독하는 프로그램(PC용)

import paho.mqtt.subscribe as subscribe

topics = ['RPi/SWITCH-1'] #토픽
print('Topic: ', topics[0])
broker = "test.mosquitto.org"

while True:
    m = subscribe.simple(topics, hostname=broker,
                         retained=False, msg_count=1)
    print('Message: ', m.payload.decode())#라즈베리 파이의 메시지 출력