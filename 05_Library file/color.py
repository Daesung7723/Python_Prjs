import time

COLOR_ADD = 0x53
COLOR_REG = 0x00
COLOR_R = 0x10
COLOR_G = 0x0D
COLOR_B = 0x13

class color():
    def __init__(self, i2c):
        self.i2c = i2c
        temp1 = bytearray(2)
        temp1[0] = 0x00
        temp1[1] = 0x06
        self.i2c.writeto(COLOR_ADD,temp1)
        temp2 = bytearray(2)
        temp2[0] = 0x04
        temp2[1] = 0x41
        self.i2c.writeto(COLOR_ADD,temp2)
        temp3 = bytearray(2)
        temp3[0] = 0x05
        temp3[1] = 0x01
        self.i2c.writeto(COLOR_ADD,temp3)

    def GetColor(self):
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_R]))
        buff_R = self.i2c.readfrom_mem(COLOR_ADD,COLOR_R,2)
        Red = buff_R[1]*255+buff_R[0]
        
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_G]))
        buff_G = self.i2c.readfrom_mem(COLOR_ADD,COLOR_G,2)
        Green = buff_G[1]*255+buff_G[0]
        
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_B]))
        buff_B = self.i2c.readfrom_mem(COLOR_ADD,COLOR_B,2)
        Blue = buff_B[1]*255+buff_B[0]
        
        if Red > 2300:
            Red = 2300
        if Green > 4600:
            Green = 4600
        if Blue > 2700:
            Blue = 2700
        
        Red = Red*255/2300
        Green = Green*255/4600
        Blue = Blue*255/2700
        
        if Red == Green:
            if Red == Blue:
                Red = 255
                Green = 255
                Blue = 255
        elif Red > Green:
            if Red > Blue:
                Red = 255
                Green = Green/2
                Blue = Blue/2
        elif Green > Red:
            if Green > Blue:
                Red = Red/2
                Green = 255
                Blue = Blue/2
        elif Blue > Red:
            if Blue > Green:
                Red = Red/2
                Green = Green/2
                Blue = 255
        Color = [Red,Green,Blue]
        return Color


    def GetRGBValue(self):
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_R]))
        buff_R = self.i2c.readfrom_mem(COLOR_ADD,COLOR_R,2)
        Red = buff_R[1]*255+buff_R[0]
        
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_G]))
        buff_G = self.i2c.readfrom_mem(COLOR_ADD,COLOR_G,2)
        Green = buff_G[1]*255+buff_G[0]
        
        self.i2c.writeto(COLOR_ADD,bytearray([COLOR_B]))
        buff_B = self.i2c.readfrom_mem(COLOR_ADD,COLOR_B,2)
        Blue = buff_B[1]*255+buff_B[0]
        
        if Red > 2300:
            Red = 2300
        if Green > 4600:
            Green = 4600
        if Blue > 2700:
            Blue = 2700
        
        Red = Red*255/2300
        Green = Green*255/4600
        Blue = Blue*255/2700
        
        Color = [Red,Green,Blue]
        return Color

