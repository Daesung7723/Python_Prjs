#펄스 카운트 프로그램(라즈베리 파이)

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

broker = "test.mosquitto.org"

#에지 변화가 감지되면 호출되는 콜백
def mycallback(channel):
    global count, flag, SEG, topics
    
    count += 1
    if count == 10:
        flag = 0 #감지 중지
        GPIO.output(18, 1) #LED ON
        return
    
    print('Button {} pressed'.format(count))
    
    #7-segment에 표시하기 위해 4자리 2진수로 변환
    LEDbit = bin(count).split('b')[1].zfill(4)
    #7-segment에 펄스 수 표시
    for i in range(4):
        GPIO.output(SEG[i], int(LEDbit[i]))
        
    publish.single(topics[0], str(count),
                   hostname=broker)
        
SEG = [26,19,13,6] #A4, A3, A2, A1 for 7-segment
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.IN) #펄스 입력 핀
GPIO.setup(18, GPIO.OUT) #LED를 출력모드로 설정
GPIO.output(18, 0) #LED OFF

for i in SEG: #7-segment 연결 핀 초기화
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 0) #처음에는 OFF

count = 0 #펄스 수
flag = 1 #flag = 0이 되면 감지를 중지한다
topics = ['control/pulse', 'control/state']
publish.single(topics[0], "0", hostname=broker)
publish.single(topics[1], "Running", hostname=broker)

#2번 핀에서 상승 모서리 감지
GPIO.add_event_detect(2, GPIO.RISING, callback=mycallback)

while flag == 1: #신호 감지 계속
    continue

GPIO.remove_event_detect(2) #감지 해제
print('The END')