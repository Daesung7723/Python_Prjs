# requests 모듈을 이용한 GET request 프로그램

import requests

while True:
    setting = input("LED on? or off?: ")
    
    #서버로 request 전송
    #라즈베리파이 주소 = 10.0.0.1
    resp = requests.get("http://10.0.0.1:8080/", params = {"led": setting})
    print(resp.text) #라즈베리파이 응답