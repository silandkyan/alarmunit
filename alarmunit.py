 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""
from time import time
from machine import Pin, Timer, ADC, PWM
from Alarm import Alarm
from mcp_pin_class import mcp_pin
from buzzer_class import buzzer


### INITIALIZE I2C BUS ###
# creating bus-instance
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq = 100000)

# define device address on i2c-bus
device = 0x20

### PINS ###
# Input Pins
pin_dig1 = Pin(16, Pin.IN)
pin_dig2 = mcp_pin(i2c, device, 'b0', 'IN')
pin_dig3 = mcp_pin(i2c, device, 'b7', 'IN')
pin_analog = ADC(Pin(26))
analog_error_threshold = 32000

# Output Pins
led_dig1 = mcp_pin(i2c, device, 'a7', 'OUT')
led_dig2 = Pin(15, Pin.OUT)
led_dig3 = mcp_pin(i2c, device, 'a5', 'OUT')
led_analog = mcp_pin(i2c, device, 'a6', 'OUT')
buzzer_1 = buzzer(PWM(Pin(14)), 600, 200)


### CREATE ALARM CLASS ###
A = Alarm()

### ACTIONS ### 
L1 = A.Action('L1', led_dig1, norm_out=1)
L2 = A.Action('L2', led_dig2, norm_out=0, delay = 3, persistent=True)
L3 = A.Action('L3', led_dig3, norm_out=0)
L4 = A.Action('L4', led_analog, norm_out=0, delay = 3, persistent=True)
L5 = A.Action('L5', buzzer_1, norm_out=0)




### SENSORS ###
S1 = A.Sensor('S1', pin_dig1, 'digital', norm_val=0, actions=[L1, L5])

S2 = A.Sensor('S2', pin_dig2, 'digital', norm_val=1, actions=[L2])

S3 = A.Sensor('S3', pin_dig3, 'digital', norm_val=0, actions=[L3, L5])

S_adc = A.Sensor('S_adc', pin_analog, 'analog', analog_error_threshold, actions=[L4])


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
