import machine

class buzzer:
    '''class for adapting passive buzzer to machine functions.
       Special implementation for module Alarm.
       taken arguments:
           pin: syntax: PWM(Pin(pin)); type = int; uses machine.PWM for pinmode
           freq1/2: type = int; takes frequence in Hz for melody'''
    def __init__(self, pin, freq1, freq2):
        self.pin = pin
        self.melody = [freq1, freq2]
        self.index = 0
        
    def on(self):
        self.index = ~self.index # changes frequency after each iteration/callback from alarmunit
        self.pin.duty_u16(10000) # setup for buzzer
        self.pin.freq(self.melody[abs(self.index)]) # play selected frequency

    def value(self):
        val = self.pin.duty_u16()
        if val == 10000:
            return 1
        elif val == 0:
            return 0
    
    def off(self):
        self.pin.duty_u16(0)

        