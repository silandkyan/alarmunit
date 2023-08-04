#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

class Error:

    error_list = []
    instance_list = []

    @classmethod
    def handle_no_errors(cls, pin_out):
        '''Check for active errors. If all is okay, emit a signal for 
        a status LED. In case of error, no signal is emitted.'''
        for inst in cls.instance_list:
            # print(inst.pin_in, inst.active_error) # status message
            if inst.active_error == True:
                inst.error_list.append(inst)
        
        if len(cls.error_list) == 0:
            print('green on')
            pin_out.on()
        else:
            print(cls.error_list)
            pin_out.off()
        
        cls.error_list = []

            
    def __init__(self, pin_in, pin_out, error_value):
        '''Init takes pin objects from the machine module of Micropython.
        Parameters:
            pin_in: Pin object for the input signal; can be analog 
                or digital pin.
            pin_out: Pin object for the output signal; must be digital pin. 
            error_value: value of digital or analog error signal
                digital case: 0 or 1, whichever is considered as error.
                analog case: int value above which input is considered as error.'''
        self.pin_in = pin_in
        self.pin_out = pin_out
        self.error_value = error_value
        Error.instance_list.append(self)
        
    def check_digital(self):
        if self.pin_in.value() == self.error_value:
            self.pin_out.on()
            self.active_error = True
            print('Error')
        else:
            self.pin_out.off()
            self.active_error = False
            
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value >= self.error_value:
            self.pin_out.on()
            self.active_error = True
        else:
            self.pin_out.off()
            self.active_error = False 

            
            