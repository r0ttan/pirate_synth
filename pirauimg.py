import sys, signal

import RPi.GPIO as GPIO
from PIL import Image
import ST7789 as ST7789

print("""
image.py - Display an image on the LCD.
If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the rear slot.
""")

BUTT = [5, 6, 16, 20]
LABL = ['A', 'B', 'X', 'Y']
IMGLIST = ['maxpi.jpg', 'ebapi.jpg']
IMGINDX = 0
images = []

#if len(sys.argv) >= 2:
#    image_file = sys.argv[1]
#else:
#    image_file = IMGLIST[IMGINDX%2]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

for i in IMGLIST:
    t_image = Image.open(i)
    rez_image = t_image.resize((WIDTH, HEIGHT))
    images.append(rez_image)

# Initialize display.
disp.begin()

def handle_butt(pin):
    global IMGINDX
    label = LABL[BUTT.index(pin)]
    print(f"Button {label} pressed on pin: {pin}")
    if label == 'B':
        IMGINDX -= 1
    elif label == 'Y':
        IMGINDX += 1
    #image_file = IMGLIST[IMGINDX%2]
    # Load an image.
    print('Loading image: {}...'.format(images[IMGINDX%2]))
    #image = Image.open(image_file)

    # Resize the image
    #image = image.resize((WIDTH, HEIGHT))

    # Draw the image on the display hardware.
    print('Drawing image')

    disp.display(images[IMGINDX%2])


for pin in BUTT:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_butt, bouncetime=100)



signal.pause()
