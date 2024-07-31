# MicroPython TM1650 driver, I2C and SPI interfaces

import time
from machine import Pin

class ultrasonic():
    def __init__(self, _Trig, _Echo):
        self.Trig = _Trig
        self.Echo = _Echo
            
    def Distance(self):
        self.Trig.value(0)
        time.sleep(0.000002)
        self.Trig.value(1)
        time.sleep(0.000015)
        self.Trig.value(0)
        t2 = 0
        while not self.Echo.value():
            t1 = 0
        t1 = 0
        while self.Echo.value():
            t2 += 1

        time.sleep(0.001)
        #print ("distance_1 is %d " % ((t2 - t1)* 2.0192))
        return ((t2 - t1)* 2.0192/10)

    def Distance_accurate(self):
        num = 0
        ultrasonic = []
        while num < 5:
                distance = self.Distance()
                #print("distance is %f"%(distance))
                while int(distance) == -1 :
                    distance = self.Distance()
                    #print("Tdistance is %f"%(distance) )
                while (int(distance) >= 500 or int(distance) == 0) :
                    distance = self.Distance()
                    #print("Edistance is %f"%(distance) )
                ultrasonic.append(distance)
                num = num + 1
                time.sleep(0.01)
        distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3
        #print("distance is %f cm"%(distance) ) 
        return int(distance)


