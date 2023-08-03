#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

class Error:
    
    #error_digital = False
    #error_analog = False
    # two seperate class variables, because of interference from digital and analog error.
    # green LED is only enabled if there is no error.

    error_list = []
    instance_list = []

    
    @classmethod
    def handle_no_errors(cls, pin_out):
        for inst in cls.instance_list:
            print(inst.pin_in, inst.active_error)
            if inst.active_error == True:
                inst.error_list.append(inst)
        if len(cls.error_list) == 0:
            print('green on')
            pin_out.on()
        else:
            print(cls.error_list)
            pin_out.off()
        cls.error_list = []
            
        #if not Errors:
            #pin_out.on()
        #else:
            #pin_out.off()
        
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

            
            