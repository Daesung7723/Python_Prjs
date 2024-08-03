# 메시지를 수신하여 LED를 제어하고,
# 스위치의 상태를 메시지로 송신하는 프로그램(라즈베리 파이)

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

LED = 18 #GPIO18 = LED
SWITCH = 23 #GPIO23 = 스위치
broker = "test.mosquitto.org" #MQTT 브로커 주소
# broker = "broker.hivemq.com"

def Rpi_Set():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(SWITCH, GPIO.IN)
    GPIO.output(LED, GPIO.LOW) # 초기에 LED OFF

#브로커와 연결되면 실행되는 콜백 함수
def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("RPi/LED")

# 메시지를 수신하면 실행되는 콜백 함수
def On_Message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(msg.topic+" "+cmd)
    
    if cmd == "ON": # LED ON
        GPIO.output(LED, GPIO.HIGH)
    elif cmd == "OFF": # LED OFF
        GPIO.output(LED, GPIO.LOW)
    else:
        print("Invalid message")

client = mqtt.Client() #클라이언트 객체 생성
client.on_connect = On_Connect #연결 콜백 함수 지정
client.on_message = On_Message #메시지 수신 콜백 함수 지정

client.connect(broker, 1883, 60) #브로커 연결
client.loop_start() #이벤트 루프 시작

while True:
    state = GPIO.input(SWITCH) #스위치 상태 읽기
    if state == 1:
        s_msg = "SWITCH ON"
    else:
        s_msg = "SWITCH OFF"
        
    client.publish("RPi/SWITCH", s_msg) #스위치 상태 메시지 발행
    time.sleep(2)