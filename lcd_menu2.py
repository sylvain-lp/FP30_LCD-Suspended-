#!/usr/bin/python3

# requires RPi_I2C_driver.py
import RPi_I2C_driver
# RPi I2C commands
LCD_CLEARDISPLAY	= 0x01
ROTARY_RIGHT_PIN	= 9
ROTARY_LEFT_PIN		= 11
ROTARY_BUTTON_PIN	= 10

from datetime import datetime
from time import sleep, time
import RPi.GPIO as GPIO
from encoder  import *
#from FP30_Instruments import instruments, FP30_Instruments
from FP90_Instruments import instruments, FP90_Instruments

# Global Variable for For Menu Item Selection
value = 1
menu =  0 # Placeholder for LCDMenu object

class LCDMenu:
	# Initialize object & LCD
	# Globa Variable for For Menu Item Selection
	global value

	def __init__(self, menu_text, lcd_rows=4, lcd_cols=20):
		self.menu_text	= menu_text
		self.lcd_rows	= lcd_rows
		self.lcd_cols	= lcd_cols
		self.lcd		= RPi_I2C_driver.lcd() # Initialize LCD Display
		self.lcd.lcd_clear() 
		self.menu_sel 	= 1 # Menu Line Selected (1 = 1st Item)
		self.menu_max	= lcd_rows
		self.page		= 0 # Menu Pagination (0 = force show 4 menu items on start)
		self.instrument_selection_value	= 1 # Memorize Value
		# LCD Text will be displayed outside of __init__ method (to prevent writting twice)
		# self.lcd.lcd_display_string_pos(self.menu_text, 1, 2)
		self.custo_chr = [[0b00000, # Define Custom CURSOR for Menu
				   0b01110,
				   0b11111,
				   0b11111,
				   0b11111,
				   0b01110,
				   0b00000,
				   0b00000]]  # [ 0x00, 0x00, 0x03, 0x04, 0x08, 0x19, 0x11, 0x10 ]]
		self.lcd.lcd_load_custom_chars(self.custo_chr)

		self.menu_char = chr(0) #unichr(0) #chr(0) # chr(126) # ">"
		# LCD Menu Selector will be displayed outside of __init__ method (to prevent displaying twice)
		# self.lcd.lcd_display_string_pos(self.menu_char, self.menu_sel, 0) # Display selector on 0,0
		self.lcd.backlight(1) # Turn on LCD Backlight
		# self.movepage(1) # List 1st 4 items of 1st page of Menu (ie. menu_max rows) 
		# LCD Menu Items will be displayed outside of __init__ method (to prevent displaying twice)
		# self.list_menu_items(1)  # List 1st 4 items of 1st page of Menu (ie. menu_max rows) 
	"""
	def up(self): # Move Menu Selector UP
		self.lcd.lcd_display_string_pos(" ", self.menu_sel, 0) 	# Clear current cursor position
		if self.menu_sel > 1:	# If cursor not at top of screen, move UP
			self.menu_sel -= 1
		else:
			self.menu_sel = self.menu_max 	# If cursor at top, restart bottom of screen
		self.lcd.lcd_display_string_pos(self.menu_char, self.menu_sel, 0)

	def down(self): # Move Menu Selector DOWN
		self.lcd.lcd_display_string_pos(" ", self.menu_sel, 0)       # Clear current cursor position
		if self.menu_sel >= self.menu_max:   # If cursor at bottom of screen, move to TOP
				self.menu_sel = 1 
		else:
				self.menu_sel += 1   # If cursor not at bottom of scree, move DOWN
		self.lcd.lcd_display_string_pos(self.menu_char, menu_sel, 0)
	"""
	def movepage(self,value): # Move SELECTOR in MENU, using 4-Line Pagination
		self.new_page = ((value - 1) // self.menu_max) + 1	# Calculate Current Page for SELECTOR (ie. value / 4)
		# print("DEBUG: Page: %d was: %d, value: %d" % (self.new_page, self.page, value))
		print("DEBUG: Value: %2d Page: %2d Select: %2d (prev_page: %2d)" % (value, self.new_page, ((value - 1) % self.menu_max) + 1,self.page ))
		# Clear current cursor position
		self.lcd.lcd_display_string_pos(" ", self.menu_sel, 0)  

		# Calulate new SELECTOR Position: UP/DOWN on Same page, UP=4th on PREVIOUS page or DOWN=1st on NEXT page
		self.menu_sel = ((value - 1) % self.menu_max) + 1

		if self.new_page != self.page:	# If SELECTOR moves to PREVIOUS or NEXT Page, display new Menu Items on Page 
			# Display PAGE if it has CHANGED from CURRENT (to Prev / Next)
			self.list_menu_items(value)
			self.page = self.new_page	# Memorize NEW Page Number

		# Show New CURSOR Position + Memorize new Page Number & Instrument Selection Value
		self.lcd.lcd_display_string_pos(self.menu_char, self.menu_sel, 0)
		self.instrument_selection_value = value

	def list_menu_items(self,value):
		# Identify Top Menu Item to List ("value" can be item at botton of screen)
		self.top_item = ((value-1) // self.menu_max * self.menu_max) + 1
		for i in range(self.menu_max):
			self.display_string_pos(instr.get_item(self.top_item + i), i + 1, 1)

	def move(self,value): # Move Menu Selector UP/DOWN
		self.lcd.lcd_display_string_pos(" ", self.menu_sel, 0)  # Clear current cursor position
		self.menu_sel = (value % self.menu_max) + 1 # Using Rotarty Value Modulo 4 (screen size) to display Menu Cursor
		self.lcd.lcd_display_string_pos(self.menu_char, self.menu_sel, 0)  # self.menu_sel, 0)
		# self.lcd.lcd_display_string_pos("%s %c" % ("Value:", value), 3, 2) # Display LCD special character
		# self.lcd.lcd_display_string_pos("%s %d  " % ("Value:", value), 3, 2) # Display Numeric value of Rotary Button

	def display_string_pos(self, menu_text, row, pos):	# Display Text on LCD at (row, pos)  - NO POS CONTROL !
		self.lcd.lcd_display_string_pos(menu_text, row, pos)

	def load_custom_chars(self, fontdata):
		self.lcd.lcd_load_custom_chars(fontdata)

	# def display_value(self, value):
		#self.lcd.lcd_display_string_pos("%s %s" % ("Value:", self.menu_sel), 3, 2)
		#print("Row: %s\tValue: %s" % (self.menu_sel, value))

	def backlight(self, value):
		self.lcd.backlight(value)

# Callback when ROTARY Button is ROTATED
def valueChanged(rotation): #, push_event): # Rotary Button  Moved
	global value			# for Menu Item Selection
	
	# Do nothing if ROTARY Position is the SAME
	if rotation != value:

	# Prevent Rotary from selecting NEGATIVE Values
		if value < 1:
			value = 1
		else:
			value = rotation
			menu.movepage(value)

		print("Rotation: ",rotation)

# Initiate Encoder & Selection Value
# BCM Rotary Pin 11 & 9 = Physical Pin 23 & 21 (Rpi B.Rev 2). PUSH BTN Pin 10 (Physical 19)
enc1 = Encoder(11,9,10,valueChanged)	
# value = 1 # Selection Value
prev  = 0 # Previous Position of Menu Pointer [>]

# Get Time (should be reboot time)
now = datetime.now()

# Initiate Rotary Encoder
GPIO.setmode(GPIO.BCM)

try:
	# sleep(5)
	instr = FP90_Instruments(instruments)
	print("DEBUG", instr.get_item(value))

	# Create LCD / Menu instance
	menu = LCDMenu(instr.get_item(value)) 
	
	# Display 1st Page of Menu Items
	menu.movepage(value)

	# Detecting when Rotary is PUSHED and trigger CALLBACK ("button_event" function from Encoder class)
	GPIO.add_event_detect(enc1.SWITCH_PIN, GPIO.RISING, callback=enc1.button_event, bouncetime=300)

	# Initializing Interrupts for Rotary Directions Pins A, B & PUSH BUTTON
	GPIO.add_event_detect(ROTARY_LEFT_PIN,  GPIO.BOTH, callback=enc1.transitionOccurred) #, bouncetime=300)
	GPIO.add_event_detect(ROTARY_RIGHT_PIN, GPIO.BOTH, callback=enc1.transitionOccurred) #, bouncetime=300) 

	# Display Menu Slector on 1st Item / 1st Page (start Value = 1)
	valueChanged(value)

	# Main LOOP - Wait for Rotary events
	while True:
		sleep(5)

# Exit on CTRL-C: Clean Screen + Turn Backlight OFF + Rotary LED OFF
except KeyboardInterrupt:	# Ctrl-C to terminate the program
	enc1.led_red(False)		# Turn Encoder LED OFF (Red LED OFF)
	enc1.led_green(False)	# Turn Encoder LED OFF (Green LED OFF)
	enc1.led_blue(False)	# Turn Encoder LED OFF (Blue LED OFF)
	menu.lcd.lcd_clear()	# Clean characters from LCD
	GPIO.cleanup()			# Clean Encoder
	sleep(1)
	print("Program Stopped - Bye!")
	menu.backlight(0)		# Turn LCD Backlight OFF
