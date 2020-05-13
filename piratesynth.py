import sys, signal

import RPi.GPIO as GPIO
from PIL import Image
import ST7789 as ST7789

"""
Intended to use on a headless raspberrypi zero without network,
together with a pirateaudio hat (Like the Headphone Amp). Uses the
lcd and buttons on the pirate audio hat. With small modifications it
could probably run on a bare raspberrypi or other audio hats.
"""
splash = 'jollyrog240.jpg'
BUTTON = [5, 6, 16, 20] #GPIO pins (BCM)
BLABEL = ['A', 'B', 'X', 'Y'] #Labels on the pirateaudio hat
COLOR = {'red': (181, 35, 22), 'orange':(184, 114, 22),
        'yellow': (183, 186, 22), 'green': (20, 184, 28),
        'blue': (18, 159, 184), 'indigo': (19, 16, 181),
        'violet': (129, 14, 179)}
HUE = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Buttons connect to ground when pushed, apply pull_up

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

WIDTH = disp.width
HEIGHT = disp.height

splash_image = Image.open(splash)
if splash_image.widht > 240 and splash_image.height > 240:
    splash_image = splash_image.resize((WIDTH, HEIGHT))

# Initialize display.
disp.begin()
disp.display(images[IMGINDX%2])

image = Image.new("RGB", (240, 240), (181, 35, 22))
draw = ImageDraw.Draw(image)

def handle_button(pin):
    global HUE
    if label == 'B':
        HUE -= 0.01
    elif label == 'Y':
        HUE += 0.01

    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    print(f'Hue: {HUE} = RGB: {(r, g, b)}')
    draw.rectangle((0, 0, 240, 240), (r, g, b))
    st7789.display(image)



for pin in BUTTON:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_butt, bouncetime=125)

signal.pause()
