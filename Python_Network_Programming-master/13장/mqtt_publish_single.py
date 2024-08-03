# publish.single() 함수를 사용한 단일 메시지 발행 프로그램

import paho.mqtt.publish as publish

#topic="mqtt/test"
topic = "TestTopic" #토픽
payload = "Hello Everyone" #발행 메시지
broker = "test.mosquitto.org" #브로커 주소

publish.single(topic, payload, hostname=broker) #메시지 발행
print("message published")
