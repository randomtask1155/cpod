#!/usr/bin/python3
import time
import os

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trellis = NeoTrellis(i2c_bus)

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

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

def playSound(event):
    os.system("play " + soundMap[event.number])

def toggleLED(event):
    if ledMap[event.number]:
        trellis.pixels[event.number] = OFF 
        ledMap[event.number] = False
    else:
        trellis.pixels[event.number] = CYAN
        ledMap[event.number] = True
        

# this will be called when button events are received
def blink(event):
    if event.edge == NeoTrellis.EDGE_RISING:
        toggleLED(event)
        if ledMap[event.number]:
            playSound(event)

def initPurple():
    for i in range(16):
        trellis.pixels[i] = PURPLE
        time.sleep(0.05)
    for i in range(16):
        trellis.pixels[i] = OFF
        time.sleep(0.05)
 

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
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)

