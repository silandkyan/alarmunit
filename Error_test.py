#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

class Error:
    error_active = False
    
    @classmethod
    def handle_no_errors(cls, pin_out):
        if not cls.error_active:
            pin_out.on()
        else:
            pin_out.off()
            
    def __init__(self, pin_in, pin_out, error_value):
        self.pin_in = pin_in
        self.pin_out = pin_out
        self.error_value = error_value
    
    def check_digital(self):
        if self.pin_in.value() == self.error_value:
            self.pin_out.on()
            Error.error_active = True
        else:
            self.pin_out.off()
            Error.error_active = False
    
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value > self.error_value:
            self.pin_out.on()
            Error.error_active = True
        else:
            self.pin_out.off()
            Error.error_active = False
            