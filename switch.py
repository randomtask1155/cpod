#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pushpin = 6
GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(pushpin, GPIO.IN)

while True:
    input_state = GPIO.input(pushpin)
    if input_state == True:
        print("switch on")
        time.sleep(.2)
    else:
        print("switch off")
        time.sleep(.2)

