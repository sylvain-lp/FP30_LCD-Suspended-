# requires RPi_I2C_driver.py
import RPi_I2C_driver
# RPi I2C commands
LCD_CLEARDISPLAY = 0x01

from datetime import datetime
from time import sleep, time
import RPi.GPIO as GPIO
from encoder  import *
#from FP30_Instruments import instruments, FP30_Instruments
from FP90_Instruments import instruments, FP90_Instruments

class LCDMenu:
# Initialize object & LCD
	def __init__(self, menu_text, lcd_rows=4, lcd_cols=20):
		self.menu_text	= menu_text
		self.lcd_rows	= lcd_rows
		self.lcd_cols	= lcd_cols
		self.lcd		= RPi_I2C_driver.lcd() # Initialize LCD Display
		self.lcd.lcd_clear() 
		self.menu_sel 	= 1 # Menu Line Selected (1 = 1st Item)
		self.menu_max	= lcd_rows
		self.page		= 1 # Menu Pagination (2 = force show 4 menu items on start)
		self.instrument_selection_value	= 1 # Memorize Value
		self.lcd.lcd_display_string_pos(self.menu_text, 1, 2)
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
		self.lcd.lcd_display_string_pos(self.menu_char, self.menu_sel, 0) # Display selector on 0,0
		self.lcd.backlight(1) # Turn on LCD Backlight
		# self.movepage(1) # List 1st 4 items of 1st page of Menu (ie. menu_max rows) 
		self.list_menu_items(1)  # List 1st 4 items of 1st page of Menu (ie. menu_max rows) 

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

	def movepage(self,value): # Move SELECTOR in MENU, using 4-Line Pagination
		self.new_page = ((value - 1) // self.menu_max) + 1	# Calculate Current Page for SELECTOR (ie. value / 4)
		# print("DEBUG: Page: %d was: %d, value: %d" % (self.new_page, self.page, value))
		print("DEBUG: Value: %2d Page: %2d Select: %2d" % (value, self.new_page, ((value - 1) % self.menu_max) + 1 ))
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

	def display_value(self, value):
		#self.lcd.lcd_display_string_pos("%s %s" % ("Value:", self.menu_sel), 3, 2)
		print("Row: %s\tValue: %s" % (self.menu_sel, value))

	def backlight(self, value):
		self.lcd.backlight(value)

	# DELETE - Only testing if Function can be called as a Callback from an Interrupt inside Encoder Class
	def buttonEvent(self, channel): 
		print("The Button was Pressed - Value=%2d - Selected: %s" % (self.instrument_selection_value, instr.get_item(self.instrument_selection_value)))

# Initiate Encoder & Value
value = 1
prev  = 0 # Previous Position of Menu Pointer [>]

# Get Time (should be reboot time)
now = datetime.now()

# Initiate LCD Display
#mylcd = RPi_I2C_driver.lcd()

# Initiate Rotary Encoder
GPIO.setmode(GPIO.BCM)



def valueChanged(value): #, push_event): # Rotary Button  Moved
#	global prev
#	mylcd.lcd_display_string_pos(" ", prev, 1)  # Clear Pointer [>]
#        mylcd.lcd_display_string_pos(">", value, 0)  # Move Pointer to new position 
#	mylcd.lcd_display_string(" %s %s" % ("Value: ", value), 3)
#	prev = value # Store Pointer Position
# 	
	""" 	if enc1.push_event() == BUTTON_LONG_PRESS:
				value = 1
				# enc1.push_event = BUTTON_RELEASED
				menu.movepage(value) """
	
	if value > 0:
		menu.display_value(value) # Print ROTARY VALUE to Console
		# Paginate through Menu Items & Move SELECTOR
		menu.movepage(value)
	else:
		value = 1


	# # Move CURSOR up/down to SELECT MENU ITEM - NO SCROLLING (if same page)
	# if value > 0 and value < 4:
	# 	menu.move(value) # Move Menu CURSOR on next/previous ITEM on SAME PAGE
	

	# 	menu.display_value("%d mod4 = %d" % (value, value % menu.menu_max +1))
	# 	menu.lcd.lcd_write(LCD_CLEARDISPLAY)	# Clear all characters from LCD screen
	# 	for i in range(4):
	# 		menu.display_string_pos(instr.get_item(value+i), i+1, 1)
    # 		# print("* New value: {}".format(value))
	# else:
	# 	value = 0
	# 	menu.display_string_pos("-- TOP MENU --", 1, 1)


#GPIO.setmode(GPIO.BOARD)   # Initialize Encode, Using physical pin numbering

# BCM Rotary Pin 11 & 9 = Physical Pin 23 & 21 (Rpi B.Rev 2). PUSH BTN Pin 10 (Physical 19)
enc1 = Encoder(11,9,10,valueChanged)	

# enc1.led_blue(True)	    # Turn Encoder BLUE (Blue LED ON)
# enc1.led_blue(True)	    # Turn Encoder BLUE (Blue LED ON)
# enc1.led_blue(True)	    # Turn Encoder BLUE (Blue LED ON)

try:
	# sleep(5)
	instr = FP90_Instruments(instruments)
	print("DEBUG", instr.get_item(1))
	menu = LCDMenu(instr.get_item(1)) # Create LCD / Menu instance

	# DELETE - Only test for GPIO on Button Event outside Encoder Class
	GPIO.add_event_detect(enc1.SWITCH_PIN, GPIO.RISING, callback=menu.buttonEvent, bouncetime=300)

	#	mylcd.backlight(1)
	# Initialize LCD with TOP 4 MENU ITEMS
	#menu.movepage(value) # Move on 1st page, to show 4 menu items
	
	#for i in range(4):
	#	menu.display_string_pos(instr.get_item(value+i), i+1, 1)

	while True:
		sleep(5)
	# print("Prev Value: {}".format(prev)) 
	# print("New  Value: {}".format(enc1.getValue()))
	# sleep(60) # 2 sec delay

# Clear Screen + Turn Backlight OFF + Rotary LED OFF
except KeyboardInterrupt:	# Ctrl-C to terminate the program
	enc1.led_red(False)		# Turn Encoder LED OFF (Red LED OFF)
	enc1.led_green(False)	# Turn Encoder LED OFF (Green LED OFF)
	enc1.led_blue(False)	# Turn Encoder LED OFF (Blue LED OFF)
	menu.lcd.lcd_clear()	# Clean characters from LCD
	GPIO.cleanup()			# Clean Encoder
	sleep(1)
	print("Program Stopped - Bye!")
	menu.backlight(0)		# Turn LCD Backlight OFF
