from machine import Pin
import utime

relay = Pin(4, Pin.OUT)

# The relay is opened, COM and NO are connected on the relay, and COM and NC are disconnected.
def relay_on():
    relay(1)

# The relay is closed, the COM and NO on the relay are disconnected, and the COM and NC are connected.
def relay_off():
    relay(0)

# Loop, the relay is on for one second and off for one second
while True:
    relay_on()
    utime.sleep(1)

    relay_off()
    utime.sleep(1)
