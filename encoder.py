# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO
from time import sleep, time

RED_LED_PIN   = 22 # ( 15 Physical Pin / 22 BCM Pin)
GREEN_LED_PIN = 27 # ( 13 Physical Pin / 27 BCM Pin)
BLUE_LED_PIN  = 17 # ( 11 Physical Pin / 17 BCM Pin)

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

        # Initializing Rotary Encoder Directions Pins A, B & PUSH BUTTON
        # SLP: Replaced PUD_DOWN with PUD_UP for A & B since my ROTARY ENCODER expects UP
        GPIO.setup(self.leftPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Rotary A
        GPIO.setup(self.rightPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Rotary B
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Push Button

       # SLP: Initialize RGB LEDs - turn BLUE (R & G are left OFF)
        GPIO.setup(RED_LED_PIN,   GPIO.OUT, initial=GPIO.HIGH)   # Set LED pins to be Output pins and initial value: high (off)
        GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=GPIO.HIGH)   # Set LED pins to be Output pins and initial value: high (off)
        GPIO.setup(BLUE_LED_PIN,  GPIO.OUT, initial=GPIO.LOW)    # Set LED pins to be Output pins and initial value: LOW (ON)

        # Initializin Interrupts for Rotary Directions Pins A, B & PUSH BUTTON
        GPIO.add_event_detect(self.leftPin,   GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.rightPin,  GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.buttonPin, GPIO.RISING, callback=self.button_event, bouncetime=200)

 
        # SLP: Added LED Actions
    def led_red(self, active = False):
        if active == False:
            GPIO.output(RED_LED_PIN, GPIO.HIGH) # Turn RED LED OFF
        else:
            GPIO.output(RED_LED_PIN, GPIO.LOW) # Turn RED LED ON
            self.active = True

    def led_green(self, active = False):
        if active == False:
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH) # Turn GREEN LED OFF
        else:
            GPIO.output(GREEN_LED_PIN, GPIO.LOW) # Turn GREEN LED ON
            self.active = True

    def led_blue(self, active = False):
        if active == False:
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH) # Turn BLUE LED OFF
        else:
            GPIO.output(BLUE_LED_PIN, GPIO.LOW) # Turn BLUE LED ON
            self.active = True

    # Button Events - PUSHED & RELEASED + DEBOUNCE using TIMER
    def button_event(self,buttonPin):
        # buttonState = GPIO.input(buttonPin) 
        #if buttonState == 1:
            # event = BTN_RELEASED # self.BUTTONUP
        # else:
        #    print("BUTTON is RELEASED:", buttonState)
       
        start = time() #start timer
        # print("last:", self.stop, "now:", start, "delta:", start - self.stop)

        # If BOUNCE CALL, then RETURN
        if (start - self.stop) < 0.24:
            print("SKIPPING Bounce call - delta: ", start - self.stop )
            return
        else:
            # BUTTON starts as SHORT PUSH - TURNED GREEN
            self.led_blue(False) # Turn off BLUE Light
            self.led_green(True) # BUTTON is GREEN when SHORT PUSH
            sleep(0.20)
            while((GPIO.input(buttonPin) == 1) and (time() - start < 1)): #always loop if button pressed
                sleep(0.04)
                self.stop = time() #stop timer
            # AFTER SHORT PRESS, TURN BUTTON back to BLUE
            self.led_green(False) 
            if (time() - start) < 1:
                self.led_blue(True)
                print("SHORT PRESS: %.2f ms" % (time() - start))
            # AFTER LONG PRESS, TURN BUTTON to RED
            else:
                self.led_red(True)
                print("LONG PRESS: %.2f ms" % (time() - start))
                sleep(2)
                self.led_red(False)
                self.led_blue(True)

            # sleep(0.20)
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

