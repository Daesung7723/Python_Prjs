# callback() 함수를 이용한 메시지 구독 프로그램

import paho.mqtt.subscribe as subscribe

#메시지가 수신되면 실행되는 콜백 함수
def on_message(client, userdata, message):
    '''
    인자들은 모두 모듈 내부의 이벤트 루프에 의해 설정된다
    client=모듈이 생성하는 클라이언트 객체
    userdata=callback() 함수의 userdata
    message=수신 메시지의 토픽과 내용
    '''
    print("%s %s" % (message.topic, message.payload))

subscribe.callback(on_message, "mqtt/test",
                   hostname="test.mosquitto.org")