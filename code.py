import random
import math
import time
import board
import digitalio
import audioio
import busio
import adafruit_vl53l0x
import adafruit_thermistor
import neopixel

#########################
#-- slide switch to enable/disable running loop
slide_switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)

#########################
#-- Audio setup
spkren = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkren.switch_to_output()
spkren.value = 0
audioout = audioio.AudioOut(board.SPEAKER)
laugh1 = audioio.WaveFile(open("laugh1.wav", "rb"))
laugh2 = audioio.WaveFile(open("laugh2.wav", "rb"))
laughs = [laugh1, laugh2]
music1 = audioio.WaveFile(open("thriller16k.wav", "rb"))
music2 = audioio.WaveFile(open("ghostbusters16k.wav", "rb"))
musics = [music1, music2]

#-- intialise random generator
temp = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
seed = int(math.modf(temp.temperature)[0]*10000000)
random.seed(seed)

#########################
#-- Distance sensor
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#########################
#-- neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
orange = (255, 75, 0)
colors = [(0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255),
          (0, 0, 255), (255, 0, 255), (255, 255, 255)]
maxbright = 0.7
pixels.brightness = 0.0
pixels.fill(orange)

#########################
#-- animation 1

def anim1(audioout):
    pixels.fill(orange)
    while not audioout or audioout.playing:
        pixels.brightness = maxbright
        time.sleep(0.15)
        pixels.brightness = 0.0
        time.sleep(0.2)

def anim2(audioout):
    pixels.fill(colors[0])
    while not audioout or audioout.playing:
        pix1 = random.randrange(10)
        pix2 = random.randrange(10)
        while pix2 == pix1:
            pix2 = random.randrange(10)
        pix3 = random.randrange(10)
        while pix3 == pix1 or pix3 == pix2:
            pix3 = random.randrange(10)

        pixels[pix1] = colors[random.randrange(1, 8)]
        pixels[pix2] = colors[random.randrange(1, 8)]
        pixels[pix3] = colors[random.randrange(1, 8)]

        pixels.brightness = maxbright

        time.sleep(0.2)

        pixels.brightness = maxbright
        pixels[pix1] = colors[0]
        pixels[pix2] = colors[0]
        pixels[pix3] = colors[0]

#########################
#-- Main loop

def pumpkin():
    #-- Wait for trigger
    print("WAITING TRIGGER")
    distance = 1000000
    while distance > 1000:
        time.sleep(1)
        distance = vl53.range
        print("Distance: ", distance)
        random.randrange(5)

    #-- Play random laugh
    laugh = random.randrange(len(laughs))
    print("laugh: ", laugh)
    audioout.play(laughs[laugh])

    anim1(audioout)

    #-- Play random music
    music = random.randrange(len(musics))
    print("music: ", music)
    audioout.play(musics[music])

    anim2(audioout)

    print("completed")
    time.sleep(10)


while slide_switch.value:
    pumpkin()
