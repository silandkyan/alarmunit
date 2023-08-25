#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:50 2023

"""
with open('Alm_matrix.csv', encoding='iso-8859-1') as data:
        lines = data.readlines()

errors = []
dig_an = []
nc_no = []
 
for line in lines[14:32]:
    columns = line.strip().split(',')
    errors.append(columns[4])
    dig_an.append(columns[5])
    nc_no.append(columns[6])

print(errors, dig_an, nc_no)

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
        
            
    def __init__(self, pin_in, error_type, error_row, error_value, no_error_value):
        self.pin_in = pin_in
        self.error_type = error_type
        self.error_row = error_row
        self.error_value = error_value
        self.no_error_value = no_error_value
        self.open_alm_matrix()
        
    #def persistent_error(self):
        #for pin in self.pins_out:
            #if pin.error_active == True:
                '''if persistent error true, set global variable True to "break" timer
                callback function'''
                #Error.persist_error == True
                #print('Persistent error:',str(self),'occured, please resolve and press error solved button!')
    
    #@classmethod
    #def error_resolved(cls, pin_resolved):
        '''reset alarms button as input pin/argument here'''
        # NOTE: will only work with Schalter, not Taster, or Taster has to be pressed for a whole interation of timer
        #if pin_resolved.value() == 1:
            #Error.persist_error == False
            #print('Persistent error resolved callback function active!')
        
    def check_digital(self):
        if self.pin_in.value() == self.error_type:
            for i in range(len(self.error_value)/2)
                Error.matrix[self.error_row][self.error_value[i]] = self.error_value[i+1]
        
            #for pin in self.pins_out:
                #pin.on()
            #self.active_error = True
        else:
            for pin in self.pins_out:
                pin.off()
            self.active_error = False
            
    def check_analog(self):
        analog_value = self.pin_in.read_u16()
        if analog_value >= self.error_type:
            self.pins_out.on()
            self.active_error = True
        else:
            self.pins_out.off()
            self.active_error = False 

        
        
                        
                        
        
                    
                    
                    
                    
                    
                