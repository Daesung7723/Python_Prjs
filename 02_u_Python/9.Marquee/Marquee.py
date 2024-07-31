import ws2812b
import random
import utime

ring_pin = 17 # Mdoule connect pin
numpix   = 8  # Number of RGB lights
# Initialize RGB light halo
strip = ws2812b.ws2812b(numpix, 0, ring_pin)
strip.fill(0,0,0) # Clear RGB buffer
strip.show()      # Refresh display

while True:
    for i in range(numpix):
        strip.fill(0,0,0)
        r = random.randint(0, 256)
        g = random.randint(0, 256)
        b = random.randint(0, 256)

        strip.set_pixel(i, r, g, b)
        strip.show()
        utime.sleep(.2)
