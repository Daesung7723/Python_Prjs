from machine import Pin
import utime

led = Pin(25, Pin.OUT)
sound = Pin(28, Pin.IN)

# Turn on the LED light that comes with the Pico board
def led_on():
    led.value(1)

# Close the LED light that comes with the Pico board
def led_off():
    led.value(0)

# Read the state of the sound module, 
# Return True if the sound exceeds the threshold, 
# Return False if it does not exceed the threshold
def sound_state():
    if sound.value() == 0:
        return True
    return False

# Main loop function, detect the sound module, 
# If the threshold is exceeded, the LED light is turned on, otherwise it is turned off
while True:
    if sound_state() == True:
        print("get sound")
        led_on()
        utime.sleep(.1)
    else:
        led_off()
