#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

class Error:
    def __init__(self, pin_in, pin_out, error_value):
        self.pin_in = pin_in
        self.pin_out = pin_out
        self.error_value = error_value
    
    def check_digital(self):
        if self.pin_in.value() == self.error_value:
            self.pin_out.on()
            # AllOff(ON)
        else:
            self.pin_out.off()
    
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value > self.error_value:
            self.pin_out.on()
            # AllOff(ON)
        else:
            self.pin_out.off()