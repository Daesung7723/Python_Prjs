from machine import Pin
import utime

# Initialize the vibration motor module
shake = Pin(12, Pin.OUT)

# Vibration sensor on
# on_time is the opening time, and delay_time is the delay time after closing.
# The time unit is milliseconds, a positive integer.
def shake_on(on_time, delay_time):
    shake.value(1)
    utime.sleep_ms(on_time)
    shake.value(0)
    utime.sleep_ms(delay_time)

while True:   
    shake_on(100, 100)
    shake_on(100, 100)
    shake_on(100, 300)
    shake_on(500, 1000)
    