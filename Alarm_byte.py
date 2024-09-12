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
            action.triggers = action.triggers & 0x1


    @classmethod
    def run_actions(cls):
        for action in cls.actions:
            action.eval_state()
            action.prepare_output()  
            action.set_output()
    
    
    @classmethod
    def check_all_ok(cls):
        for action in cls.actions:
            if action.pin_ok is not None: 
                val = action.pin_out.value() # read value of action.pin_out
                if val == action.norm_out: # actual value of action.pin_out is equal to action.norm_out
                    action.pin_ok.on() # ok
                elif val != action.norm_out: # actual value of action.pin_out is not equal to action.norm_out
                    action.pin_ok.off() # not ok
            if action.pin_all_ok is not None:
                if cls.Action.all_ok != 0x0: # check for possible error yielded from action.set_output()
                    action.pin_all_ok.off() # there is at least one error: not ok
                else:
                    action.pin_all_ok.on() # there is no error: ok
        cls.Action.all_ok = cls.Action.all_ok & 0x1 # resets byte, AND operation yields 0x1 if persistent error, else 0x0
            
            
    @classmethod
    def admin_operation(cls):
        for master in cls.masters:
            master.reset_or_ignore()
        
        
    class Sensor:
        index = 0 # used to save the information: which sensors have which action
        def __init__(self, name, pin_in, input_type, norm_val, actions):
            '''Class for managing sensors, monitoring their state and 
            connecting them to Action objects.
            Parameters:
                name: str; descriptive name 
                pin_in: Pin object; (from the machine module of Micropython) 
                    for the input signal; can be analog or digital pin.
                input_type: str; "digital" or "analog"
                norm_val: int; value of digital or analog normal signal on pin_in.
                    digital: 0 or 1, whichever is considered as normal.
                    analog: value below which input is considered as normal.
                actions: list of Action objects to be triggered by this Sensor.'''
            self.name = name
            self.pin_in = pin_in
            self.input_type = input_type
            self.norm_val = norm_val
            self.actions = actions
            Alarm.sensors.add(self)
            Alarm.Sensor.index += 1
            self.index = Alarm.Sensor.index
            for action in self.actions: 
                action.index_byte |= (1 << self.index) # which sensors have a certain action in self.actions 
        
        
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
            if val != self.norm_val:
                self.write_to_actions(1)
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
            '''Overrides values given by check functions to action.triggers on the bit
            corresponding to the index of the measured sensor. If any actions for particular
            this sensor should be ignored, its corresponding bit in action.triggers is always 0
            which means no error.'''
            for action in self.actions:
                if (action.index_byte & Alarm.Master.actions) & (1 << self.index) == (1 << self.index): 
                    action.triggers &= ~(1 << self.index)
                else:
                    action.triggers |= (value << self.index)
            
            
    class Action:
        all_ok = 0x0 # cls.all_ok is list for saving status of output pins
        index = 0
        def __init__(self, name, pin_out, norm_out, pin_ok=None, pin_all_ok=None, delay=None, persistent=False):
            '''Class for managing Action objects and their output behaviour.
                name: str; descriptive name
                pin_out: Pin object; (from the machine module of Micropython) 
                    for the output signal; must be digital pin.
                norm_out: int; 1 (on) or 0 (off); signal written to pin_out if 
                    state is normal.
                pin_ok: Pin object; status depends on status of pin_out; optional
                pin_all_ok: Pin object; common pin for all instances of Action; optional
                delay (optional): int; time in sec to wait before out signal switches 
                    to error mode.
                persistent (optional): True or False; Error object is treated as 
                    persistent or not.
                    
                index_byte: hex; stores information which sensors the action listens to:
                            if action_x.index_byte & (1 << sensor_y.index) == (1 << sensor_y.index):
                                => action_x listens inter alia to sensor_y.
                triggers: hex; stores information about errors. State of sensor_y
                          get written on bit in triggers corresponding to sensor_y.index
                          => triggers byte holds info for error: 0 / 1 on sensor_y.'''
            self.name = name
            self.pin_out = pin_out
            self.norm_out = norm_out
            self.pin_ok = pin_ok
            self.pin_all_ok = pin_all_ok
            self.delay = delay
            self.persistent = persistent
            self.index_byte = 0x0
            self.triggers = 0x0 
            self.curr_state = 0 # state during current iteration of main loop
            self.last_state = 0 # state during last iteration of main loop
            self.actual_state  = 0 # state actually written to pin_out
            Alarm.actions.add(self)
            Alarm.Action.index += 1
            self.index = Alarm.Action.index


        def eval_state(self):
            '''Checks if any connected sensor detected an error in the current
            iteration. If yes, the Action object switches to an internal error state.
            Bit corresponding to action in Alarm.actions.all_ok gets overwritten with value.'''
            self.last_state = self.curr_state
            if self.triggers != 0x0:
                self.curr_state = 1
            else:
                self.curr_state = 0
            Alarm.Action.all_ok |= (self.curr_state << self.index)
                    
                    
        def prepare_output(self):
            '''Prepares the Action object for setting the correct output value.
            If no delay timer is specified, this happens instantly. Otherwise,
            it manages timer operation and timed setting of the actual output.'''
            if self.delay == None:
                self.actual_state = self.curr_state
                self.set_persistent()
            else:
                # no error
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
            '''set right pin-status to pin_out depending on self.norm_out.'''
            # error
            if self.actual_state == 1:
                if self.norm_out == 1:
                    self.pin_out.off()
                elif self.norm_out == 0:
                    self.pin_out.on()
            # no error
            elif self.actual_state == 0:
                if self.norm_out == 1:
                    self.pin_out.on()
                elif self.norm_out == 0:
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
            '''Insert permanent error status in triggers and all_ok.'''
            if self.persistent == True:
                self.triggers  |= 0x1
                print('set persistent')
                Alarm.Action.all_ok |= 0x1    

                
    class Master:
        actions = 0x0
        def __init__(self, name, pin_in, norm_val, mode, object_list=None):
            '''Class for reseting all persistent alarm-outputs and for ignoring
            certain groups of alarm outputs of particular sensors.
            Parameters:
            name: str; descriptive name
            pin_in: machine.Pin object (or mcp_pin_class object)
            normal_val: int; normal value of pin_in: 0 or 1
            mode: str; either 'reset': for resetting all persistent outputs
                or 'ignore': for ingore given set of sensors
            object_list: list; optional argument for mode: 'ignore',
                takes Action-class instances which will be ignored in next iteration(s)'''
            self.name = name
            self.pin_in = pin_in
            self.norm_val = norm_val
            self.mode = mode
            self.object_list = object_list
            self.current_state = 0
            self.last_state = 0
            Alarm.masters.add(self)
            
            
        def reset_or_ignore(self):
            self.last_state = self.current_state
            val = self.pin_in.value()
            if val != self.norm_val: # check if switch state opposes the normal value
                self.current_state = 1
                if self.mode == 'reset_all':
                    self.reset_all()
                elif self.mode == 'reset_selected':
                    self.reset_selected()
            else:
                self.current_state = 0
            if self.current_state == 1 and self.last_state == 0:
                if self.mode == 'ignore':
                    self.ignore()
            elif self.current_state == 0 and self.last_state == 1:
                if self.mode == 'ignore':
                    Alarm.Master.actions = 0x0
        
        
        def reset_all(self):
            for action in Alarm.actions:
                action.triggers = 0x0 # reset all the error action.triggers to no error for this iteration
            Alarm.Action.all_ok = 0x0 
            print('all alarm-outputs reset!')
            
            
        def reset_selected(self):
            for sensor_actions in self.object_list:
                for action in sensor_actions[1:]: # iterate over the actions in the list 
                    action.triggers &= ~0x1 # reset possible persistent error 
                    action.triggers &= ~(1 << sensor_actions[0].index) # reset possible error state on bit corresponding to specifyed sensor
            Alarm.Action.all_ok = 0x0
            Alarm.run_actions()
            print('selected alarm-outputs reset!')
                
                
        def ignore(self):
            for sensor_actions in self.object_list:
                for action in sensor_actions[1:]: # iterate over the actions in the list
                    Alarm.Master.actions |= (1 << sensor_actions[0].index) # add all actions to cls.Master.actions set
                    action.triggers &= ~0x1 # reset possible persistent error 
                    action.triggers &= ~(1 << sensor_actions[0].index) # reset possible error state on bit corresponding to specifyed sensor
                action.prepare_output()
                action.set_output() # run action functions to update state
                print('output reset')
               
         