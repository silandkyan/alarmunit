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
    masters = set()
    
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
            
        if any(item == 1 for item in cls.Action.val_out): # check all no-error-LED's for status given by cls.val_out in Action 
            cls.Action.all_ok = False # if any of them is on LOW, cls.all_ok is False 
        else:
            cls.Action.all_ok = True
        cls.Action.val_out = [] # clear list of no-error LED status for next iteration
            
    @classmethod
    def admin_operation(cls):
        for master in cls.masters:
            master.reset_or_ignore()
        
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
            val = self.pin_in.value()
            if val is not None:
                if val != self.norm_val:
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
            if self in Alarm.Master.ignore_list: # hold back error outputs of sensors given by cls.ignore_list in Master
                if value == 0:
                    for action in self.actions:
                        action.triggers.append(0)
                if value == 1:
                    for action in self.actions:
                        action.triggers.append(0)
                        print('Error occured but output held back!')
            else:
                for action in self.actions:
                    action.triggers.append(value)                 
                
    class Action:
        val_out = [] # cls.val_out is list for saving status of no-error-LED's 
        all_ok = True # cls.all_ok is True or False depending on whether there are errors or not. Default is no error = True!
        def __init__(self, name, pin_error, norm_out, pin_ok, pin_all_ok, delay=None, persistent=False):
            '''Class for managing Action objects and their output behaviour.
                name: str; descriptive name
                pin_error: Pin object (from the machine module of Micropython) 
                    for the output signal; must be digital pin.
                norm_out: 1 (on) or 0 (off); signal written to pin_error if 
                    state is normal.
                pin_ok: Pin object; status depends on status of pin_error
                pin_all_ok: Pin object; common pin for all instances of Action
                delay: None or time in sec to wait before out signal switches 
                    to error mode; optional.
                persistent: True or False; Error object is treated as 
                    persistent or not; optional.'''
            self.name = name
            self.pin_error = pin_error
            self.pin_ok = pin_ok
            self.pin_all_ok = pin_all_ok
            self.norm_out = norm_out
            self.err_out = abs(self.norm_out - 1) # TODO: not needed?
            self.delay = delay
            self.persistent = persistent
            self.triggers = [0] # list of states of connected sensors; 0=good, 1=bad
            self.curr_state = 0 # state during current iteration of main loop
            self.last_state = 0 # state during last iteration of main loop
            self.actual_state  = 0 # state actually written to pin_error
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
            '''Sets proper output value for errors depending on normal value and Action state.'''
            if self.actual_state == 0:
                if self.norm_out == 0:
                    self.pin_error.off()
                elif self.norm_out == 1:
                    self.pin_error.on()
            elif self.actual_state == 1:
                if self.norm_out == 0:
                    self.pin_error.on()
                elif self.norm_out == 1:
                    self.pin_error.off()
            # check if error occured by controlling output value of self.pin_error.
            val = self.pin_error.value()
            if val is not None:
                Alarm.Action.val_out.append(val)
                if val == 0:
                    if self.norm_out == 0:
                        self.pin_ok.on()
                    elif self.norm_out == 1:
                        self.pin_ok.off()
                elif val == 1:
                    if self.norm_out == 0:
                        self.pin_ok.off()
                    elif self.norm_out == 1:
                        self.pin_ok.on()
            # check if there is ANY error or not. If not, set self.pin_all_ok High.
            if Alarm.Action.all_ok == True:
                self.pin_all_ok.on()
            elif Alarm.Action.all_ok == False:
                self.pin_all_ok.off()
        
                       
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
                
                
    class Master:
        ignore_list = [] # cls.ignore_list is list for ignorable sensors: their outputs will be held back in next iteration(s)
        def __init__(self, name, pin_in, norm_val, mode, sensor_set=None):
            '''Class for reseting all persistent alarm-outputs and for ignoring
            certain groups of Sensor-instances along with their alarm-outputs.
            Parameters:
            name: str; descriptive name
            pin_in: machine.Pin object (or mcp_pin_class object)
            normal_val: int; normal value of pin_in: 0 or 1
            mode: str; either 'reset': for resetting all persistent outputs
                or 'ignore': for ingore given set of sensors
            sensor_set: list; optional argument for mode: 'ignore',
                takes Sensor-class instances which will be ignored in next iteration(s)'''
            self.name = name
            self.pin_in = pin_in
            self.norm_val = norm_val
            self.mode = mode
            self.sensor_set = sensor_set
            Alarm.masters.add(self)
        
        def reset_or_ignore(self):
            if self.mode == 'reset':
                val = self.pin_in.value()
                if val is not None:
                    if val != self.norm_val: # check if switch state contradicts the normal value
                        self.reset_persistent_output(list(Alarm.sensors_all))
                        print('all persistent alarm-outputs reset!')
                
            elif self.mode == 'ignore':
                val = self.pin_in.value()
                if val is not None:
                    if val != self.norm_val: # check if switch state contradicts the normal value
                        Alarm.Master.ignore_list = self.sensor_set # ignore given sensors in self.sensor_set given in __init__() of Master
                        print('ignoring sensor(s):',list(map(lambda instance: instance.name, self.sensor_set))) # print every sensor which will be ignored in next iteration(s)
                        self.reset_persistent_output(self.sensor_set) 
                    elif val == self.norm_val:
                        Alarm.Master.ignore_list = [] # reset list of ignorable sensors if switch is on normal status
                
        def reset_persistent_output(self, re_set):
            print('reset persistent alarm-outputs:')
            for sensor in re_set:
                for action in sensor.actions: 
                    action.triggers = [0, 0] # reset persistent outputs 
                    print(action.name)
            
###
         