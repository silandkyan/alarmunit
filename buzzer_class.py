from machine import Timer

class buzzer:
    index = 0 # class.index is used to switch frequencies in melody
    '''class for adapting passive buzzer to machine functions.
       Special implementation for module Alarm.
       taken arguments:
           pin: syntax: PWM(Pin(pin)); type = int; uses machine.PWM for pinmode
           freq1/2: type = int; takes frequence in Hz for melody'''
    def __init__(self, pin, freq1, freq2):
        self.pin = pin
        self.melody = [freq1, freq2]
        
    def on(self):
        buzzer.index = ~buzzer.index # changes frequency after each iteration/callback from alarmunit
        self.pin.duty_u16(10000) # setup for buzzer 
        self.pin.freq(self.melody[abs(buzzer.index)]) # play selected frequency
        
    def off(self):
        self.pin.deinit()
        
        