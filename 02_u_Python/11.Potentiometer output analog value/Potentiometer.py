from machine import ADC
import utime
# Initialize the potentiometer to pin 28 (ADC function)
rp = ADC(28)

# Read the current analog value of the potentiometer and return [0, 100]
def get_value():
    return int(rp.read_u16() * 101 / 65536)

# Print the current value of the potentiometer cyclically, value=[0, 100]
while True:
    value = get_value()
    print(value)
    utime.sleep(.1)
