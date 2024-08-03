# 간단한 mqtt 메시지 구독 프로그램

import paho.mqtt.subscribe as subscribe

topics = ['mqtt/test', 'TestTopic'] #어느 것이나 구독
broker = "test.mosquitto.org"

m = subscribe.simple(topics, hostname=broker,
                     retained=False, msg_count=1)
print('Topic: ', m.topic) #토픽
print('Message: ', m.payload.decode()) #메시지