# FP30_LCD
Software for Raspberry Pi to Control Roland FP-30 Midi Keyboard using LCD Screen & Rotary RGB Encoder - written in Python
Objectives: 
1) Display & Select available instruments, Change Volume, BPM
2) Add advanced features: chord recognition
3) Add access to hidden controls available on Roland FP-30 Keyboard (instruments, sounds, controls, drums)
4) Add existing python Midi tools (sequencer ?). See work from "Yummy Mudcake"
            

Hardware used:
- Raspberry Pi Model B rev. 2 (2011.12) - 26 Pins
- LCD I2C Screen 20x4 Blue Backlight - Address 0x27
- Sparkfun Rotary Encoder - Illuminated RGB - Ref. COM-15141 ROHS 


Usefull Links:
- ROTARY ENCODER
  - https://qbalsdon.github.io/circuitpython/rotary-encoder/python/led/2021/02/27/rgb-rotary-encoder.html
  - https://www.sparkfun.com/products/15141
  - https://github.com/sparkfun/Rotary_Encoder_Breakout-Illuminated/blob/main/Firmware/RGB_Rotary_Encoder/RGB_Rotary_Encoder.ino
  
- RASPBERRY PI GPIOs
  - https://raspberry-projects.com/pi/pi-hardware/raspberry-pi-model-b/model-b-io-pins
  
- ROLAND CORP. MIDI IMPLEMENTATION Reference
  - https://static.roland.com/assets/media/pdf/FP-30_MIDI_Imple_e01_W.pdf
  - https://static.roland.com/assets/media/zip/FP-30X_MIDI_Imple_eng01_W.pdf
  - https://static.roland.com/assets/media/pdf/FP-90_FP-60_MIDI_Imple_eng02_W.pdf
  
- FP-30 GREAT WORK from 
  - "Ymmy Mudcake" (seems "gone" in Oct. 2021) - https://synthesizer-explorations.blogspot.com/2019/02/Roland-FP-30-hidden-secrets.html
  - "JJulio" - https://jjulio.github.io/FP30playground/
  
