#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:11:09 2023

@author: pgross
"""
from machine import Timer

class Alarm:
    sensors = set()
    actions = set()
    
    @classmethod
    def check_sensors(cls):
        for sensor in cls.sensors:
            sensor.check_sensor()
            
    @classmethod
    def reset_action_triggers(cls):
        '''Resets the non-permanent parts of all action trigger lists to 
        prepare a new iteration.'''
        for action in cls.actions:
            action.triggers = action.triggers[0:1]
        
    @classmethod
    def run_actions(cls):
        for action in cls.actions:
            action.eval_state()
            action.prepare_output()
            action.set_output()

    class Sensor:
        def __init__(self, name, pin_in, input_type, norm_val, actions):
            '''Class for managing sensors, monitoring their state and 
            connecting them to Action objects.
            Parameters:
                name: str; descriptive name 
                pin_in: Pin object (from the machine module of Micropython) 
                    for the input signal; can be analog or digital pin.
                input_type: "digital" or "analog"
                norm_val: value of digital or analog normal signal on pin_in.
                    digital case: 0 or 1, whichever is considered as normal.
                    analog case: int value below which input is considered as normal.
                actions: list of Action objects to be triggered by this Sensor.'''
            self.name = name
            self.pin_in = pin_in
            self.input_type = input_type
            self.norm_val = norm_val
            self.actions = actions
            Alarm.sensors.add(self)
        
        def check_sensor(self):
            '''Checks the current sensor state (good=0, bad=1) and writes
            this state to the connected Action objects.'''
            if self.input_type == "digital":
                self.check_digital()
            elif self.input_type == "analog":
                self.check_analog()
            else:
                print('Wrong input type!')
            
        def check_digital(self):
            value = self.pin_in.value()
            if value is not None:
                if value != self.norm_val:
                    self.write_to_actions(1)
                    print('Error detected!')
                else:
                    self.write_to_actions(0)
                
        def check_analog(self):
            analog_value = self.pin_in.read_u16()
            if analog_value >= self.norm_val:
                self.write_to_actions(1)
                print('Error detected!')
            else:
                self.write_to_actions(0)
            
        def write_to_actions(self, value):
            for action in self.actions:
                action.triggers.append(value)
                
                
    class Action:
        def __init__(self, name, pin_out, norm_out, delay=None, persistent=False):
            '''Class for managing Action objects and their output behaviour.
                name: str; descriptive name
                pin_out: Pin object (from the machine module of Micropython) 
                    for the output signal; must be digital pin.
                norm_out: 1 (on) or 0 (off); signal written to pin_out if 
                    state is normal.
                delay: None or time in sec to wait before out signal switches 
                    to error mode; optional.
                persistent: True or False; Error object is treated as 
                    persistent or not; optional.'''
            self.name = name
            self.pin_out = pin_out
            self.norm_out = norm_out
            self.err_out = abs(self.norm_out - 1) # TODO: not needed?
            self.delay = delay
            self.persistent = persistent
            self.triggers = [0] # list of states of connected sensors; 0=good, 1=bad
            self.curr_state = 0 # state during current iteration of main loop
            self.last_state = 0 # state during last iteration of main loop
            self.actual_state  = 0 # state actually written to pin_out
            Alarm.actions.add(self)
            
        def eval_state(self):
            '''Checks if any connected sensor detected an error in the current
            iteration. If yes, the Action object switches to an internal error state.'''
            self.last_state = self.curr_state
            if any(item == 1 for item in self.triggers):
                self.curr_state = 1
            else:
                self.curr_state = 0
                
        def prepare_output(self):
            '''Prepares the Action object for setting the correct output value.
            If no delay timer is specified, this happens instantly. Otherwise,
            it manages timer operation and timed setting of the actual output.'''
            if self.delay == None:
                self.actual_state = self.curr_state
                self.set_persistent()
            else:
                # no error:
                if self.curr_state == 0 and self.last_state == 0:
                    self.actual_state = self.curr_state
                # new error, set timer
                elif self.curr_state == 1 and self.last_state == 0:
                    self.set_timer()
                # no error anymore, stop timer
                elif self.curr_state == 0 and self.last_state == 1:
                    self.acttimer.deinit() 
                    print('timer off')
                    
        def set_output(self):
            '''Sets proper output value depending on normal value and Action state.'''
            if self.actual_state == 0:
                if self.norm_out == 0:
                    self.pin_out.off()
                elif self.norm_out == 1:
                    self.pin_out.on()
            elif self.actual_state == 1:
                if self.norm_out == 0:
                    self.pin_out.on()
                elif self.norm_out == 1:
                    self.pin_out.off()
                    
        def set_timer(self):
            '''Creates an internal Timer object for the output delay.'''
            print('timer on')
            self.acttimer = Timer(-1)
            self.acttimer.init(period=self.delay*1000,
                               mode=Timer.ONE_SHOT, callback=self.actiontimer)
                
        def actiontimer(self, timer):
            '''Defines what happens on timer callback.'''
            self.actual_state = self.curr_state
            self.set_persistent()
            
        def set_persistent(self):
            if self.persistent == True:
                self.triggers[0] = self.actual_state
                print('set persistent')
                
###
         