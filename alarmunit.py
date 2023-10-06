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

# get devices connected to i2c-bus 
mcp_pin.scan_devices(i2c)

# define device addresses on i2c-bus
device_1 = 0x20
device_2 = 0x21

### PINS ###

# Input Pins
pin_mcp_dig1 = mcp_pin(i2c, device_1, 'a7', 'IN')
pin_mcp_dig2= mcp_pin(i2c, device_1, 'b0', 'IN')
pin_reset_persistent = Pin(11, Pin.IN)
pin_ignore_sensors = Pin(12, Pin.IN)
# pin_pico_analog = ADC(Pin(26))
# analog_error_threshold = 32000

# Output Pins
led_mcp_dig1 = mcp_pin(i2c, device_2, 'a7', 'OUT')
led_mcp_dig2 = mcp_pin(i2c, device_2, 'b0', 'OUT')
# led_mcp_analog = mcp_pin(i2c, device_1, 'a5', 'OUT')
# led_pico1 = Pin(15, Pin.OUT)
buzzer_1 = buzzer(PWM(Pin(14)), 500, 200)
buzzer_2 = buzzer(PWM(Pin(13)), 600, 100)


### CREATE ALARM CLASS ###
A = Alarm()

### ACTIONS ### 
L1 = A.Action('L1', led_mcp_dig1, norm_out=0)
L2 = A.Action('L2', led_mcp_dig2, norm_out=0)
# L3 = A.Action('L3', led_mcp_analog, norm_out=0, delay = 3, persistent = True)
# L4 = A.Action('L4', led_pico1, norm_out=0)
L5 = A.Action('L5', buzzer_1, norm_out=0, delay = 3, persistent = True)
L6 = A.Action('L6', buzzer_2, norm_out=0, delay = 3, persistent = True)

### SENSORS ###
S1 = A.Sensor('S1', pin_mcp_dig1, 'digital', norm_val=1, actions=[L1, L5])
S2 = A.Sensor('S2', pin_mcp_dig2, 'digital', norm_val=1, actions=[L2, L6])
#S3 = A.Sensor('S3', pin_pico1, 'digital', norm_val=0, actions=[L4])
#S_adc = A.Sensor('S_adc', pin_pico_analog, 'analog', analog_error_threshold, actions=[L3, L6])

M1 = A.Master('M1', pin_reset_persistent, norm_val=0, mode='reset')
M2 = A.Master('M2', pin_ignore_sensors, norm_val=0, mode='ignore', sensor_set=[S1, S2])

### TIMER CALLBACK FUNCTION ###
def timer_callback(timer):
    A.reset_action_triggers()
    A.check_sensors()
    A.run_actions()
    A.admin_operation()
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
