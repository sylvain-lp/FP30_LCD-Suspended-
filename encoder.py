# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO
from time import sleep, time

BLUE_LED_PIN = 22 # ( 15 Physical Pin / 22 BCM Pin)
SWITCH_PIN   = 10 # ( 19 Physical Pin / 10 BCM Pin)

BTN_PUSHED   = 100
BTN_RELEASED = 101

class Encoder:

    def __init__(self, leftPin, rightPin, buttonPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.buttonPin = buttonPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        self.stop = 0 # for Button press timer
        # SLP: Added to make sure using the right GPIO PIN (BCM/Broadcom)
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        # SLP: Replace PUD_DOWN with PUD_UP since my ROTARY ENCODER expects UP
        GPIO.setup(self.leftPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Rotary A
        GPIO.setup(self.rightPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Rotary B
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Push Button

        GPIO.add_event_detect(self.leftPin,   GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.rightPin,  GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.buttonPin, GPIO.RISING, callback=self.button_event, bouncetime=200)

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

    # Button Events - PUSHED & RELEASED
    def button_event(self,buttonPin):
        # buttonState = GPIO.input(buttonPin) 
        #if buttonState == 1:
            # event = BTN_RELEASED # self.BUTTONUP
        # else:
        #    print("BUTTON is RELEASED:", buttonState)
        start = time() #start timer
        print("last:", self.stop, "now:", start, "delta:", start - self.stop)

        if (start - self.stop) < 0.24:
            print("SKIPPING Bounce call - delta: ", start - self.stop )
            return
        else:
            sleep(0.20)
            while(GPIO.input(buttonPin) == 1): #always loop if button pressed
                sleep(0.04)
            self.stop = time() #stop timer
            print("BUTTON is RELEASED after %.2f ms" % (self.stop - start))
            sleep(0.20)
        # length = time() - start #get long time button pressed
        return

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

