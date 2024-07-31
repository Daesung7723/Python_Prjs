from machine import Pin
import utime

human = Pin(11, Pin.IN)
led = Pin(25, Pin.OUT)

abc = 0

# Turn on the LED light that comes with the board
def led_on():
    led.value(1)

# Turn off the LED light that comes with the board
def led_off():
    led.value(0)


def detect_someone():
    if human.value() == 1:
        return True
    return False

while True:
    if detect_someone() == True:
        abc += 1
        led_on()
        print("value=", abc)
        utime.sleep(1)
    else:
        if abc != 0:
            led_off()
            abc = 0

