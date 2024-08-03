# client 모듈을 이용한 라즈베리 파이 mqtt 구독 프로그램
# 수신 메시지를 분석하여 서로 다른 처리를 한다

import paho.mqtt.client as mqtt

# 서버와 연결되었을 때 실행되는 콜백 함수
def on_connect(client, userdata, flags, rc):
        print("Connectd with result code "+str(rc))

        # 구독 신청
        # 연결 될 때 마다 새로 구독 신청
        client.subscribe("Core/topic1")
        client.subscribe("Core/topic2")

# 메시지를 수신했을 때 실행되는 콜백 함수
def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if msg.payload.decode() == "Hello":
            print("Receiving message: #1, do something")

        if msg.payload.decode() == "World!":
            print("Receiving message #2, do something else")

# MQTT 클라이언트 객체를 생성하고 콜백 함수 연결
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60) #브로커 연결

client.loop_forever()