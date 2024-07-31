from machine import Pin, ADC
import utime
# Initialize the joystick module (ADC function)
rocker_x = ADC(27)
rocker_y = ADC(26)
button = Pin(28, Pin.IN, Pin.PULL_UP)

# Read the value of the X axis and return [0, 255]
def read_x():
    value = int(rocker_x.read_u16() * 256 / 65536)
    return value

# Read the value of Y axis and return [0, 255]
def read_y():
    value = int(rocker_y.read_u16() * 256 / 65536)
    return value

# Read the state of the button, press to return to True, release to return to False
def btn_state():
    press = False
    if button.value() == 0:
        press = True
    return press


# Print the current value of the potentiometer cyclically, value=[0, 255]
while True:
    value_x = read_x()
    value_y = read_y()
    state = btn_state()
    print("x:%d, y:%d, press:%s" % (value_x, value_y, state))
    utime.sleep(.1)
