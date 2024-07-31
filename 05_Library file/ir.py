import time
from machine import Pin


class ir():
    def __init__(self, _Pin):
        self.Pin = _Pin
        self.ir_repeat_cnt = 0
        self.irdata = 0xfe
            
    def Getir(self):
        if self.Pin.value() == 0:
            
            self.ir_repeat_cnt = 0
            count = 0
            while self.Pin.value() == 0:
                count += 1
                time.sleep(0.00003)

            count = 0
            while self.Pin.value() == 1 and count < 160:
                count += 1
                time.sleep(0.00003)
            print(" ")
            idx = 0
            cnt = 0
            data = [0,0,0,0]
            for i in range(0,32):
                count = 0
                while self.Pin.value() == 0 and count < 30:
                    count += 1
                    time.sleep(0.00003)

                count = 0
                while self.Pin.value() == 1 and count < 80:
                    count += 1
                    time.sleep(0.00003)

                if count > 35:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            
            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
                self.irdata = data[2]
        else:
            if self.ir_repeat_cnt > 110: 
                self.ir_repeat_cnt = 0
                self.irdata = 0xfe
            else:
                time.sleep(0.001)
                self.ir_repeat_cnt += 1
        if self.irdata != None:
            if self.irdata != 254:
                result = self.irdata
                # self.irdata = 254
                return result
        

