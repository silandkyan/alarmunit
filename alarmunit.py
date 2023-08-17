 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""
from time import time
from machine import Pin, Timer, ADC
from Alarm import Alarm

pin1 = Pin(16, Pin.IN)
pin2 = Pin(17, Pin.IN)

pin_analog = ADC(Pin(26))
analog_error_threshold = 32000

led1 = Pin(19, Pin.OUT)
led2 = Pin(20, Pin.OUT)
led_analog = Pin(21, Pin.OUT)

A = Alarm()

# L1 = A.LED(led1, persistent=False)
# L2 = A.LED(led2, persistent=False)
# L_analog = A.LED(led_analog, persistent=False)
L1 = A.Action('L1', [led1], [1], [0], False)
L2 = A.Action('L2', [led2], [1], [0], False)
L3 = A.Action('L3', [led_analog], [1], [0], True)

# weiter testen mit 2 sensoren!

S1 = A.Sensor('S1', pin1, 'digital', error_value=0, error_actions=[L2,L3], normal_actions=[L1])
# S2 = A.Sensor('S2', pin2, 'digital', error_value=0, errors=[L2], norms=[])
#S_adc = A.Sensor('S_adc', pin_analog, 'analog', analog_error_threshold, errors=[L_analog], norms=[])

# Timer callback function
def timer_callback(timer):
    print(A.sensors, '\n', A.actions)
    #print(pin_analog.read_u16())
    # Check for digital error
    for sensor in A.sensors:
        #print('err: ', sensor.error_actions)
        #print('norm:', sensor.normal_actions)
        sensor.check_sensor()
        
    print('staged err: ', A.staged_errors)
    print('staged norm:', A.staged_normals)
        
    errors = A.get_unique_actions(A.staged_errors)
    normals  = A.get_unique_actions(A.staged_normals)
    
    print('uni err: ', errors)
    print('uni norm:', normals)
    
    for action in A.actions:
        print(action)
        if action in errors:
            action.set_active()
        elif action in normals:
            action.set_active()
        else:
            action.set_normal()
        #elif action in norms and action not in errors:
        #    action.trigger_normal()
        
    # print(A.active_leds)
    # for led in A.leds:
    #     if led in A.active_leds.values():
    #         led.pin.on()
    #     else:
    #         led.pin.off()

    # Sleep is NOT needed in this implementation!
    print('time: ', time())
    

# Create a Timer object
timer = Timer(-1)  # Use the first available hardware timer (-1) on the microcontroller

# Set the timer callback function
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)
# The timer will fire every 5 seconds (5000 milliseconds) and call the 
# timer_callback function. Within these periods, not other code is executed.

# No need for a while loop if there are no additional code or operations to run
# while True:
#     pass

# Add any other code or operations you need to perform outside the main loop
