import machine
import utime

key = machine.Pin(0, Pin.IN, Pin.PULL_UP)

Led_Red = machine.Pin(1, Pin.OUT)
Led_Green = machine.Pin(2, Pin.OUT)
Led_Blue = machine.Pin(3, Pin.OUT)
Leds_list = [Led_Red, Led_Green, Led_Blue]

def press_state():
    if key.value() == 0:
        return True
    return False

def Leds(state, c):
    if state == 0:
        Leds_list[c].value(0)
    else:
        Leds_list[c].value(1)


# Close RGB light
def Leds_off():
    for i in range(len(Leds_list)) :
        Leds_list[i].value(0)

# Main loop, switch a color every 0.5s
if __name__ == '__main__':
    color = 0
    while True:
        if press_state() == True:
            print("press")
            color = (color + 1) % 3
            
        Leds_off()
        utime.sleep(.5)
        Leds(1,color)
        utime.sleep(.5)