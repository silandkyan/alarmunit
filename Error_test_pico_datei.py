#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""

class Error:
    
    error_list = []
    instance_list = []
    #persist_error = False 

    @classmethod
    def handle_no_errors(cls, pin_out):
        for inst in cls.instance_list:
            print(inst.pin_in, inst.active_error)
            if inst.active_error == True:
                
                inst.error_list.append(inst)
        if len(cls.error_list) == 0:
            pin_out.on()
        else:
            print(cls.error_list)
            pin_out.off()
        cls.error_list = []
        
            
    def __init__(self, pin_in, pins_out, error_value):
        self.pin_in = pin_in
        self.pins_out = pins_out
        self.error_value = error_value
        Error.instance_list.append(self)
        
    def persistent_error(self):
        for pin in self.pins_out:
            if pin.error_active == True:
                '''if persistent error true, set global variable True to "break" timer
                callback function'''
                Error.persist_error == True
                print('Persistent error:',str(self),'occured, please resolve and press error solved button!')
    
    #@classmethod
    #def error_resolved(cls, pin_resolved):
        '''reset alarms button as input pin/argument here'''
        # NOTE: will only work with Schalter, not Taster, or Taster has to be pressed for a whole interation of timer
        #if pin_resolved.value() == 1:
            #Error.persist_error == False
            #print('Persistent error resolved callback function active!')
            
    def check_digital(self):
        if self.pin_in.value() == self.error_value:
            for pin in self.pins_out:
                pin.on()
            self.active_error = True
        else:
            for pin in self.pins_out:
                pin.off()
            self.active_error = False
            
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value >= self.error_value:
            self.pins_out.on()
            self.active_error = True
        else:
            self.pins_out.off()
            self.active_error = False 

        
        
                        
                        
        
                    
                    
                    
                    
                    
                