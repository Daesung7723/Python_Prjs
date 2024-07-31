from machine import Pin, I2C
import utime
# i2c=I2C(0, scl=Pin(21),sda=Pin(20), freq=100000)
i2c=I2C(1, scl=Pin(19),sda=Pin(18), freq=100000)

from color import color
Color = color(i2c)

utime.sleep(1)

while True:
    Colors = Color.GetRGBValue()
    print("Get Color...")
    print("R:%3d G:%3d B:%3d"%(Colors[0], Colors[1], Colors[2]))    
    utime.sleep(1)
