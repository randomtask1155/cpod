#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
fanPin = 25
switchPin = 20
GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


fanStatus = False

GPIO.output(fanPin, 1)
time.sleep(3)
GPIO.output(fanPin, 0)


while True:
    input_state = GPIO.input(switchPin)
    if input_state == True:
        if not fanStatus:
            GPIO.output(fanPin, 1)
            fanStatus = True 
            os.system("play /home/pi/bin/sounds/effects/airlock-on.wav")
            os.system("/home/pi/bin/sounds/env-on")
    else:
        if fanStatus:
            GPIO.output(fanPin, 0)
            fanStatus = False
            os.system("play /home/pi/bin/sounds/effects/air-hiss.wav")
            os.system("/home/pi/bin/sounds/env-off")
    time.sleep(.3)
