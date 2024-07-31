import utime
from machine import Pin
from ultrasonic import ultrasonic


Echo = Pin(13, Pin.IN)
Trig = Pin(14, Pin.OUT)

ultrasonic = ultrasonic(Trig, Echo)

while True:
    distance = ultrasonic.Distance_accurate()
    print("distance is %d cm"%(distance))
    utime.sleep(.5)

