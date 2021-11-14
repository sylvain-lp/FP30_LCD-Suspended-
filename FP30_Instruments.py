#!/usr/bin/python

""" 
Raspberry Pi Rev. 2 Model B PINS
CONNECTING I2C LCD 20x04 and ROTARY ENCODER RGB SWITCH

 (LCD Pins)              (ROTARY Pins) 

 +5    GR
 v     ND
 |     |
 2  4  6  8 10 12 14 16 18 20 22 24 26
 1  3  5  7  9 11 13 15 17 19 21 23 25
    |  |                 |  |  |  |  |
    S  S                +3 GP GP GP GR
    D  C                v3 10 09 11 ND
    A  L
"""

instruments={}
""" INSTRUMENT LABEL, BANK SELECT MSB, LSB, PROGRAM CHANGE """
instruments={
    1:["Grand Piano 1",0, 68, 1],
    2:["Grand Piano 2",16, 67, 1],
    3:["Grand Piano 3",8, 66, 2],
    4:["Ragtime Piano",0, 64, 4],
    5:["Harpsichord 1",0, 66, 7],
    6:["Harpsichord 2",8, 66, 7],
    7:["E. Piano 1",16, 67, 5],
    8:["E. Piano 2",0, 70, 6],
    9:["E. Piano 3",24, 65, 5],
    10:["Clav.",0, 67, 8],
    11:["Vibraphone",0, 0, 12],
    12:["Celesta",0, 0, 9],
    13:["Synth Bell",0, 68, 99],
    14:["Strings 1",0, 71, 50],
    15:["Strings 2",0, 64, 49],
    16:["Harp",0, 68, 47],
    17:["Jazz Organ 1",0, 70, 19],
    18:["Jazz Organ 2",0, 69, 19],
    19:["Church Organ 1",0, 66, 20],
    20:["Church Organ 2",8, 69, 20],
    21:["Accordion",0, 68, 22],
    22:["Choir 1",8, 64, 53],
    23:["Jazz Scat",0, 65, 55],
    24:["Choir 2",8, 66, 53],
    25:["Choir 3",8, 68, 53],
    26:["Synth Pad",0, 64, 90],
    27:["Nylon-str.Gt",0, 0, 25],
    28:["Steel-str.Gt",0, 0, 26],
    29:["Decay Strings",1, 65, 50],
    30:["Decay Choir",1, 64, 53],
    31:["Decay Choir Pad",1, 66, 90],
    32:["Acoustic Bass",0, 0, 33],
    33:["A.Bass + Cymbl",0, 66, 33],
    34:["Fingered Bass",0, 0, 34],
    35:["Thum Voice",0, 66, 54]}

# print(instruments["21"][0], instruments["21"][2])

class FP30_Instruments:
    """ Menu Class for 20x4 LCD screen """
    
    def __init__(self, menu_items=instruments, selected_item=0):
        self.menu_items = menu_items
        self.selected_item = selected_item
        self.max_col = 20
        self.max_row = 4

    def list_items(self):
        for i in self.menu_items:
            # self._selected_item = i
            # print(i, self.label, self.bank_msb,self.bank_lsb,self.program_change) #self.menu_items[i][0])
            # print(self.get_item(i))
            print("%2d %s" % (i,self.menu_items[i][0])) # label)
            # vars(i)

    def get_item(self, i):
        # print("DEBUG: Instr.get_item[%2d]: %s" % (i, self.menu_items[i][0]))
        return("%2d %s" % (i,self.menu_items[i][0]))
        # return("%02d %-15s %3d %3d %3d" % (i, self.menu_items[i][0], self.menu_items[i][1],self.menu_items[i][2],self.menu_items[i][3]))

    @property
    def selected_item(self):
        return self._selected_item

    @selected_item.setter
    def selected_item(self, value):
        self._selected_item = value
            
    @property
    def label(self):
        return self.menu_items[self._selected_item][0]

    @property
    def bank_msb(self):
        return self.menu_items[self._selected_item][1]

    @property
    def bank_lsb(self):
        return self.menu_items[self._selected_item][2]   

    @property
    def program_change(self):
        return self.menu_items[self._selected_item][3] 

""" MAIN PROGRAM """

# lcdmenu = FP30_Instruments(instruments)

# lcdmenu.list_items()


    




