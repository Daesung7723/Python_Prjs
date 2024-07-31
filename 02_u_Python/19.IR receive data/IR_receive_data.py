from machine import Pin
import time
from ir import ir

#Configure infrared receiving pin
pin = Pin(5, Pin.IN, Pin.PULL_UP)

#Configure infrared receiver library
Ir = ir(pin)

while True:
    #Read remote control data
    value = Ir.Getir()
    if value != None:
        print(value)
