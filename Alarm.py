#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:11:09 2023

@author: pgross
"""

class Alarm:
    leds = set()
    sensors = set()
    actions = set()
    
    staged_errors = {}
    staged_normals = {}
    
    @classmethod
    def get_unique_actions(cls, staged_actions):
        unique_actions = set()
        for entry in staged_actions.values():
            unique_actions.update(entry)  
        return unique_actions
    

    class Sensor:
        def __init__(self, name, pin_in, input_type,
                     error_value, error_actions, normal_actions):
            '''Init takes pin objects from the machine module of Micropython.
            Parameters:
                name: str; descriptive name 
                pin_in: Pin object for the input signal; can be analog 
                    or digital pin.
                input_type: "digital" or "analog"
                error_value: value of digital or analog error signal on pin_in
                    digital case: 0 or 1, whichever is considered as error.
                    analog case: int value above which input is considered as error.
                error_actions: list of Action objects staged in case of incorrect input signal.
                normal_actions: list of Action objects staged in case of correct input signal.'''
            self.name = name
            self.pin_in = pin_in
            self.input_type = input_type
            self.error_value = error_value
            self.error_actions = error_actions
            self.normal_actions = normal_actions
            self.error_detected = False
            self.error_counter = 0
            Alarm.sensors.add(self)
            Alarm.staged_errors.update({self.name: set()})
            Alarm.staged_normals.update({self.name: set(self.normal_actions)})
        
        def check_sensor(self): # TODO: maybe as classmethod?
            #print(self.led_list)
            if self.input_type == "digital":
                self.check_digital()
            elif self.input_type == "analog":
                self.check_analog()
            else:
                print('Wrong input type!')
            
        def check_digital(self):
            if self.pin_in.value() == self.error_value:
                self.error_counter += 1
                self.stage_errors()
                self.unstage_normals()
                self.error_detected = True
                print('Error detected!')
            elif self.error_counter > 0:
                self.unstage_errors()
                self.stage_normals()
                self.error_detected = False
                
        def check_analog(self):
            analog_value = self.pin_in.read_u16()
            if analog_value >= self.error_value:
                self.error_counter += 1
                self.stage_errors()
                self.unstage_normals()
                self.error_detected = True
                print('Error detected!')
            elif self.error_counter > 0:
                self.unstage_errors()
                self.stage_normals()
                self.error_detected = False
                    
        def stage_errors(self):
            '''Add all error actions to staged_errors dict to prepare for execution in error mode.'''
            #print('stage err')
            Alarm.staged_errors.update({self.name: set(self.error_actions)})
            
        def unstage_errors(self):
            '''Remove error actions from staged_errors dict to prepare for execution in normal mode.
            Checks for persistent behavior.'''
            #print('unstage err')
            helperset = set()
            for error in self.error_actions:
                if error.persistent == True:
                    helperset.update(set([error]))
                    #print(helperset)
            Alarm.staged_errors.update({self.name: helperset})
        
        def stage_normals(self):
            '''Add normal actions to staged_normals dict to prepare for execution in normal mode.
            Checks for persistent behavior.'''
            #print('stage norm')
            helperset = set()
            for norm in self.normal_actions:
                if norm.persistent == False:
                    helperset.update(set([norm]))
                    #print(helperset)
            Alarm.staged_normals.update({self.name: helperset})
            
        def unstage_normals(self):
            '''Remove all normal actions from staged_normals dict to prepare for execution in error mode.'''
            #print('unstage norm')
            Alarm.staged_normals.update({self.name: set()})
            
            
    class Action: # TODO
        def __init__(self, name, pins_out, active_values, normal_values, persistent):
            '''Init takes pin objects from the machine module of Micropython.
            Parameters:
                name: str; descriptive name
                pins_out: list of Pin objects for the input signals; must be digital pin.
                active_values: list of 1 (on) or 0 (off) written to pins_out if triggered active.
                normal_values: list of 1 (on) or 0 (off) written to pins_out in case of normal operation.
                persistent: True or False if Error object is treated as persistent.'''
            self.name = name
            self.pins_out = pins_out
            self.active_values = active_values
            self.normal_values = normal_values 
            self.persistent = persistent
            Alarm.actions.add(self)
            
        def set_active(self):
            for pin, active in zip(self.pins_out, self.active_values):
                #print('active:', pin, active)
                if active == 1:
                    pin.on()
                elif active == 0:
                    pin.off()
                    
        def set_normal(self):
            for pin, norm in zip(self.pins_out, self.normal_values):
                #print('normal:', pin, norm)
                if norm == 1:
                    pin.on()
                elif norm == 0:
                    pin.off()
                

            # Alarm.active_leds.setdefault(sensor_name, set()).add(self)
            # # discard led from dict of inactive leds:
            # helperset = Alarm.inactive_leds.get(sensor_name, set())
            # helperset.discard(self)
            # Alarm.inactive_leds[sensor_name] = helperset
            
            # for helperset in Alarm.active_leds.values():
            #     Alarm.active = Alarm.active.union(helperset)
            

    class LED:
        def __init__(self, pin, persistent):
            '''
            pin: Pin object for the led signal; must be digital pin.
            '''
            self.pin = pin
            self.persistent = persistent
            self.pin.off()
            Alarm.leds.add(self)
            Alarm.inactive.add(self)

        def activate_led(self, sensor_name):
            # Alarm.active_leds.add(self)
            #print(sensor_name, 'act', self)
            # add led to dict of active leds:
            Alarm.active_leds.setdefault(sensor_name, set()).add(self)
            # discard led from dict of inactive leds:
            helperset = Alarm.inactive_leds.get(sensor_name, set())
            helperset.discard(self)
            Alarm.inactive_leds[sensor_name] = helperset
            
            for helperset in Alarm.active_leds.values():
                Alarm.active = Alarm.active.union(helperset)
            
        def deactivate_led(self, sensor_name):
            if self.persistent == False:
                #print(sensor_name, 'deact', self)
                #Alarm.active_leds.pop(sensor_name, None)
                # discard led from dict of active leds:
                helperset = Alarm.active_leds.get(sensor_name, set())
                helperset.discard(self)
                Alarm.active_leds[sensor_name] = helperset
                # add led to dict of inactive leds:
                Alarm.inactive_leds.setdefault(sensor_name, set()).add(self)
                
                for helperset in Alarm.inactive_leds.values():
                    Alarm.inactive = Alarm.inactive.union(helperset)


