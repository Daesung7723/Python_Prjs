from machine import ADC
import utime
# Initialize the photosensitive sensor pin to GP28 (ADC function)
light = ADC(28)

# Read the current analog value of the photosensitive sensor, range [0, 100]
def get_value():
    return int(light.read_u16() * 101 / 65536)

# Print the current value of the photosensitive sensor cyclically, value=[0, 100]
# The stronger the light intensity, the smaller the value.
while True:
    value = get_value()
    print(get_value())
    utime.sleep(.1)
