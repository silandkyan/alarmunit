 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""
from time import time
from machine import Pin, Timer, ADC
from Alarm import Alarm


### PINS ###
# Input Pins
pin1 = Pin(16, Pin.IN)
pin2 = Pin(17, Pin.IN)
pin_analog = ADC(Pin(26))
analog_error_threshold = 32000

# Output Pins
led1 = Pin(19, Pin.OUT)
led2 = Pin(20, Pin.OUT)
led_analog = Pin(21, Pin.OUT)


### CREATE ALARM CLASS ###
A = Alarm()


### ACTIONS ###
L1 = A.Action('L1', led1, 1)
L2 = A.Action('L2', led2, 0)
L3 = A.Action('L3', led_analog, 0)


### SENSORS ###
S1 = A.Sensor('S1', pin1, 'digital', norm_val=1, actions=[L1, L2])
S_adc = A.Sensor('S_adc', pin_analog, 'analog', analog_error_threshold, actions=[L3, L2])


### TIMER CALLBACK FUNCTION ###
def timer_callback(timer):
    A.reset_action_triggers()
    A.check_sensors()
    A.run_actions()
    # Sleep is NOT needed in this implementation!
    print('time: ', time())
    

### MAIN LOOP ###
# Create a Timer object
timer = Timer(-1)  # Use the first available hardware timer (-1) on the microcontroller

# Set the timer callback function
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)
# The timer will fire every x seconds (x000 milliseconds) and call the 
# timer_callback function.

# No need for a while loop if there are no additional code or operations to run
# while True:
#     pass

# Add any other code or operations you need to perform outside the main loop
