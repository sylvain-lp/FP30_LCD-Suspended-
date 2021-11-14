# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO
from time import sleep

BLUE_LED_PIN = 22 # ( 15 Physical Pin / 22 BCM Pin)


class Encoder:

    def __init__(self, leftPin, rightPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        # SLP: Added to make sure using the right GPIO PIN (BCM/Broadcom)
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        # SLP: Replace PUD_DOWN with PUD_UP since my ROTARY ENCODER expects UP
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)  

        # SLP: Initialize BLUE LED (off)
        GPIO.setup(BLUE_LED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set LED pin 22 to be an output pin and set initial value to low (off)

        # SLP: Added LED Actions
    def led_blue(self, active = False):
        print ("DEBUG: led ACTIVE attribute is : ",active)
        if active == False:
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH) # Turn BLUE LED OFF
            # print("Blue LED OFF")
            # sleep(1) # Pause 1 sec for Testing
        else:
            GPIO.output(BLUE_LED_PIN, GPIO.LOW) # Turn BLUE LED ON
            # print("Blue LED ON")
            # leep(1) # Pause 1 sec for Testing
        self.active = active

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.rightPin)
        p2 = GPIO.input(self.leftPin)
        newState = "{}{}".format(p1, p2)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value)
                
        self.state = newState

    def getValue(self):
        return self.value

