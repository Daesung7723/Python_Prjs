# 라즈베리파이에서 실행되는 시리얼 통신 프로그램

import serial
import time

port = input('port(/dev/serial0): ') #포트 이름
if port == '':
    port = "/dev/serial0"

#시리얼 포트 초기화
ser = serial.Serial(port, baudrate=115200, timeout = 1)

if ser.isOpen() == False: #포트가 열려있지 않으면 오픈한다
    ser.open()
    print("Now a serial port is open")
    
while True:
    msg = input('Your message: ') #송신 메시지 입력
    if msg == 'q': #'q'를 입력하면 종료
        break
    ser.write(msg.encode('utf-8')) #메시지를 바이트형으로 변환하여 전송
    time.sleep(1)
    
    if ser.readable(): #수신 데이터가 있으면
        r_msg = ser.readline() #수신 데이터를 읽는다
        print(r_msg.decode('utf-8')) #수신 메시지 출력
        
ser.close() #포트를 닫는다