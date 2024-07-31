from machine import Pin
import time
from dht11 import DHT11
#Initialize temperature and humidity pins
pin = Pin(22, Pin.OUT)
#Initialize the temperature and humidity library
dht11 = DHT11(pin)

while True:
    #Print temperature and humidity values
    print("temperature is %d ℃" % dht11.temperature)
    time.sleep(.5)
    print("humidity is %d " % dht11.humidity)
    time.sleep(.5)
