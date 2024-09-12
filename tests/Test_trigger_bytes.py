# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:46:34 2024

@author: pschw
"""

class master:
    sensors = []
    actions = []
    
    # @classmethod 
    # def call_actions(cls):
    #     for instance in cls.actions:
    #         instance.setup_actions()
            
    @classmethod 
    def call_sensors(cls):
        for instance in cls.sensors: 
            instance.index_action()
            
    @classmethod 
    def call_function(cls):
        for instance in cls.actions:
            instance.function_sub2()
        
    
    class sub1:
        index = 0
        def __init__(self, name, actions):
            self.name = name
            self.actions = actions
            master.sensors.append(self)
            master.sub1.index += 1
            self.index = master.sub1.index
            for action in self.actions: 
                action.index |= (1 << self.index)

            
    class sub2:
        def __init__(self, name):
            self.name = name 
            master.actions.append(self)
            self.index = 0x0
            self.triggers = 0x0
            
        def function_sub2(self):
            print(bin(self.index), self.triggers)
            
            
m = master()

L1 = m.sub2('L1')
L2 = m.sub2('L2')
L3 = m.sub2('L3')
L4 = m.sub2('L4')

S1 = m.sub1('S1', [L1, L2])
S2 = m.sub1('S2', [L1, L3])
S3 = m.sub1('S3', [L4, L3])


# m.call_actions()
# m.call_sensors()
m.call_function()










            
            
            