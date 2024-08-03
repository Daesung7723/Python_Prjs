# DHT11을 이용한 온습도 측정 프로그램

import sys
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
#Data is connected to GPIO3(pin=5)
GPIOpin = 3
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)
        print("Temp = {:0.1f}C Humidity = {:0.1f}".format(temperature, humidity))
        time.sleep(3)

finally:
    print("Cleaning up")
