#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

Errors = []

class Error:
    #error_digital = False
    #error_analog = False
    # two seperate class variables, because of interference from digital and analog error.
    # green LED is only enabled if there is no error.
    
    @classmethod
    def handle_no_errors(cls, pin_out):
        if not Errors:
            pin_out.on()
        else:
            pin_out.off()
    
    #@classmethod
    #def handle_no_errors(cls, pin_out):
        #if cls.error_digital or cls.error_analog:
            #pin_out.off()
            #print('turned off green')
        #else:
            #pin_out.on()
            
    def __init__(self, pin_in, pin_out, error_value):
        self.pin_in = pin_in
        self.pin_out = pin_out
        self.error_value = error_value
    
    def check_digital(self):
        if self.pin_in.value() == self.error_value:
            self.pin_out.on()
            #Error.error_digital = TRUE
            Errors.append(self.Error)
        else:
            self.pin_out.off()
            #Error.error_digital = FALSE
            Errors.remove(self.Error)
    
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value >= self.error_value:
            self.pin_out.on()
            #Error.error_analog = TRUE
            Errors.append(self.Error)
        else:
            self.pin_out.off()
            #Error.error_analog = FALSE
            Errors.remove(self.Error)

            
            