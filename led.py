#!/usr/bin/python3
import RPi.GPIO as GPIO
import neopixel
import board
import time
import os

GPIO.setmode(GPIO.BCM)
switchPin = 13
GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

OFF = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


ledStatus = False
defaultColor = WHITE
currentColor = defaultColor
defaultBrightness = 0.4
pixel_pin = board.D12
num_pixels = 77

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=defaultBrightness, auto_write=True
)

def init_seq():
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

init_seq()


while True:
    input_state = GPIO.input(switchPin)
    if input_state == True:
        if not ledStatus:
            ledStatus = True
            pixels.fill(currentColor)
            os.system("play /home/pi/bin/sounds/effects/power-on.wav")
    else:
        if ledStatus:
            init_seq()
            ledStatus = False 
            os.system("/home/pi/bin/sounds/lights-off")
    time.sleep(.3)

