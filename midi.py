#!/usr/bin/python3
import time
import os
import RPi.GPIO as GPIO
import neopixel
import board

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from random import randrange

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trellis = NeoTrellis(i2c_bus)

## sed default mode [ led || music ]
musicMode = 0
ledMode = 1
midiMode = musicMode
midiModeCache = musicMode ## set the cache state

# some color definitions
OFF = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128,0,128)
SILVER = (192,192,192)
MAROON = (128,0,0)
OLIVE= (128,128,0)
MAGENTA = (255,0,255)
TEAL = (0,128,128)
PINK = (255,105,180)
INDIGO = (75,0,130)
CHOCOLATE = (210,105,30)
STEELBLUE = (176,196,222)

musicSwitchPin = 16
ledSwitchPin = 13
ledStatus = False
musicStatus = True
defaultColor = WHITE
currentColor = defaultColor
defaultBrightness = 0.4
pixel_pin = board.D12
num_pixels = 77

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(musicSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=defaultBrightness, auto_write=True
)

secretMap = {"light": False,
             "midi": False,
             0: False,
             3: False,
             12: False,
             15: False}

def clearSecret():
    for key in secretMap:
        secretMap[key] = False

def check_secret():
    found = True
    for key in secretMap:
        if not secretMap[key]:
            found = False
    if found:
        clearSecret()
        os.system("/home/pi/bin/sounds/play-secret")
        

soundDir = "/home/pi/bin/sounds/effects/"
soundMap = {0: soundDir + 'power-on.wav',
            1: soundDir + 'lazer.wav',
            2: soundDir + 'explosion.wav',
            3: soundDir + 'scanning.wav',
            4: soundDir + 'bobbing-chiptone.wav',
            5: soundDir + 'boom.wav',
            6: soundDir + 'warp.wav',
            7: soundDir + 'ngoat.wav',
            8: soundDir + 'cat.wav',
            9: soundDir + 'charging-laser.wav',
            10: soundDir + 'space-sweep.wav',
            11: soundDir + 'yay.wav',
            12: soundDir + 'laser-shoot.wav',
            13: soundDir + 'helium.wav',
            14: soundDir + 'funny-boing.wav',
            15: soundDir + 'girl-scream.wav'}

ledMap = {0: False,
          1: False,
          2: False,
          3: False,
          4: False,
          5: False,
          6: False,
          7: False,
          8: False,
          9: False,
          10: False,
          11: False,
          12: False,
          13: False,
          14: False,
          15: False}

lightsColorMap = {0: WHITE,
        1: RED,
        2: YELLOW,
        3: GREEN,
        4: CYAN,
        5: PURPLE,
        6: SILVER,
        7: BLUE,
        8: MAROON,
        9: OLIVE,
        10: MAGENTA,
        11: TEAL,
        12: PINK,
        13: CHOCOLATE,
        14: INDIGO,
        15: STEELBLUE
}

colorMap = { 0: RED,
             1: YELLOW,
             2: GREEN,
             3: CYAN,
             4: BLUE,
             5: PURPLE}

################################### 
## LED LIGHTS FUNCTINOS
################################### 

def init_led_seq():
    pixels.fill(WHITE)
    pixels.show()
    time.sleep(0.2)
    pixels.fill(RED)
    time.sleep(0.2)
    pixels.fill(YELLOW)
    time.sleep(0.2)
    pixels.fill(GREEN)
    time.sleep(0.2)
    pixels.fill(CYAN)
    time.sleep(0.2)
    pixels.fill(PURPLE)
    time.sleep(0.2)
    pixels.fill(BLUE)
    time.sleep(0.2)
    pixels.fill(OFF)

def toggle_lights():
    global ledStatus
    input_state = GPIO.input(ledSwitchPin)
    if input_state == True:
        if not ledStatus:
            ledStatus = True
            pixels.fill(currentColor)
            initLights()
            os.system("play /home/pi/bin/sounds/effects/power-on.wav")
            secretMap["light"] = True
    else:
        if ledStatus:
            init_led_seq()
            ledStatus = False 
            initPurple()
            os.system("/home/pi/bin/sounds/lights-off")
            secretMap["light"] = False

################################### 
## NEO TRELLIS FUNCTIONS
###################################

def toggle_music():
    global musicStatus
    input_state = GPIO.input(musicSwitchPin)
    if input_state == True:
        if not musicStatus:
            initPurple()
            musicStatus = True
            secretMap["midi"] = True
    else:
        if musicStatus:
            musicStatus = False
            if ledStatus:
                initLights()
                secretMap["midi"] = False



def toggle_midistate():
    global midiMode
    ledInput = GPIO.input(ledSwitchPin)
    musicInput = GPIO.input(musicSwitchPin)
    if ledInput and not musicInput:
        midiMode = ledMode 
    else:
        midiMode = musicMode

def playSound(event):
    os.system("play " + soundMap[event.number])

def toggleLED(event):
    if ledMap[event.number]:
        trellis.pixels[event.number] = OFF 
        ledMap[event.number] = False
    else:
        trellis.pixels[event.number] = colorMap[randrange(6)]
        ledMap[event.number] = True
        
def checkMidiState():
    global midiModeCache
    print (midiMode)
    print (midiModeCache)
    if midiMode != midiModeCache:
        if midiMode == ledMode:
            initLights()
            midiModeCache = ledMode
        else: 
            if midiMode == musicMode:
                initPurple()
                midiModeCache = musicMode

# this will be called when button events are received
def blink(event):
    if event.edge == NeoTrellis.EDGE_RISING:
        if midiMode == musicMode:
            checkMidiState()
            toggleLED(event)
            if ledMap[event.number]:
                playSound(event)
                if event.number in secretMap.keys():
                    secretMap[event.number] = True
        else: 
            if midiMode == ledMode:
                checkMidiState()
                pixels.fill(lightsColorMap[event.number])

def initLights():
    for i in range(16):
        trellis.pixels[i] = lightsColorMap[i]
        time.sleep(0.05)

def initPurple():
    for i in range(16):
        trellis.pixels[i] = PURPLE
        time.sleep(0.05)
    for i in range(16):
        trellis.pixels[i] = OFF
        time.sleep(0.05)

init_led_seq() 

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = PURPLE
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

while True:
    # watch for led light state changes
    toggle_lights()
    toggle_music()
    toggle_midistate()
    check_secret()
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.3)



