# client 모듈을 이용한 메시지 발행 프로그램

import paho.mqtt.client as mqtt

client = mqtt.Client() #클라이언트 객체 생성
client.connect("test.mosquitto.org", 1883, 60) #브로커와 연결
rc, mid = client.publish("mqtt/test", "Hello Everyone") #rc=응답 코드
print(str(rc)) #응답 코드 출력