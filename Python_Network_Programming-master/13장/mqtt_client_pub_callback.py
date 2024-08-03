# client 모듈을 이용한 메시지 발행 프로그램

import paho.mqtt.client as client

broker="test.mosquitto.org"
port=1883

#메시지가 성공적으로 발행되면 호출되는 콜백
def on_publish(client1, user_data, mid):
    print("data published\n")
    pass

client1= client.Client() #클라이언트 객체 생성
client1.on_publish = on_publish #on_publish 속성에 콜백 함수 연결
client1.connect(broker, port) #브로커와 연결
ret= client1.publish("mqtt/test","Hello") #메시지 발송