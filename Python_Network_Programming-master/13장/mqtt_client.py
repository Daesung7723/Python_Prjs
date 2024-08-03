# client 모듈을 이용한 메시지 구독 프로그램

import paho.mqtt.client as mqtt

# 브로커와 연결되면 실행되는 콜백
def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 이 부분에서 구독 신청을 하면 연결이 끊어지더라도 재연결된다
    topic = "mqtt/test"
    client.subscribe(topic)

# 메시지가 도착하면 실행되는 콜백
def On_Message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client() #클라이언트 객체 생성
client.on_connect = On_Connect #연결 콜백 지정
client.on_message = On_Message #메시지 콜백 지정

client.connect("test.mosquitto.org", 1883, 60) #브로커와 연결

# 이벤트 루프 시작
client.loop_forever()
