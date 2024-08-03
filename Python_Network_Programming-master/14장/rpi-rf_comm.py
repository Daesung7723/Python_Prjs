# 시리얼 통신을 이용한 블루투스 통신 프로그램

import serial
import time

port="/dev/rfcomm0" #SPP를 위한 통신 포트
print('hello world')
bluetooth= serial.Serial(port,9600)#객체 생성
print ('hello world 2')
bluetooth.flushInput()#버퍼를 비운다
print ('hello world 3')

for i in range(100):
    print("we are in the for loop",i)
    bluetooth.write("a".encode()) #문자 송신
    inputs=bluetooth.readline() #응답 수신
    print("we are in the inputs for loop",i)
    inputasinteger= int(inputs)
    if inputs:
            print('we have inputs')
            fileb= open("blue.txt",'wU') #파일 오픈
            fileb.write(inputasinteger*10)#파일에 수신 응답을 저장
    time.sleep(.5)
    print('sleeping')
    
fileb.close() #파일을 닫는다
print('file has been closed')
exit()