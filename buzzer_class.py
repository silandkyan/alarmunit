from Alarm import Alarm
from utime import sleep

class buzzer:
    
    def __init__(self, pin, freq_1, freq_2, on_off):
        self.on_off = on_off
        self.pin = pin
        self.freq = [freq_1, freq_2]
        
    def on(self):
        if self.on_off.triggers[0] == self.on_off.actual_state:
            for f in self.freq:
                self.pin.duty_u16(10000)
                self.pin.freq(f)
                sleep(0.5)
        else:
            self.off()
        
    def off(self):
        self.pin.deinit()
        
        