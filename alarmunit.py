 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""
from time import time
from machine import Pin, Timer, ADC, PWM
from Alarm_byte import Alarm
from mcp_pin_class import mcp_pin
from buzzer_class import buzzer

### BUG REPORT/QUESTIONS 12.09.24 ###
# - test with analog sensor!
# - with Alarm_byte 50 Hz are okay for current circuit

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
pin_mcp_dig2 = mcp_pin(i2c, device_1, 'b0', 'IN')
pin_mcp_dig3 = mcp_pin(i2c, device_1, 'b2', 'IN')
pin_reset_persistent = mcp_pin(i2c, device_1, 'a6', 'IN')
pin_ignore_sensors = mcp_pin(i2c, device_1, 'b1', 'IN')
# pin_pico_analog = ADC(Pin(26))
# analog_error_threshold = 32000

# Output Pins
relais1 = mcp_pin(i2c, device_2, 'a7', 'OUT')
relais1_ok = mcp_pin(i2c, device_2, 'a5', 'OUT')
relais2 = mcp_pin(i2c, device_2, 'b0', 'OUT')
relais2_ok = mcp_pin(i2c, device_2, 'a6', 'OUT')

error_led1 = mcp_pin(i2c, device_2, 'a3', 'OUT')
error_led2 = mcp_pin(i2c, device_2, 'a2', 'OUT')
error_led3 = mcp_pin(i2c, device_2, 'b1', 'OUT')
buzzer_1 = buzzer(PWM(Pin(14)), 500, 200)
buzzer_2 = buzzer(PWM(Pin(13)), 600, 100)

led_all_ok = mcp_pin(i2c, device_2, 'a4', 'OUT')
# led_mcp_analog = mcp_pin(i2c, device_1, 'a5', 'OUT')


### CREATE ALARM CLASS ###
A = Alarm()

### ACTIONS ### 
L1 = A.Action('L1', relais1, norm_out=1, pin_ok=relais1_ok, pin_all_ok=led_all_ok)
L2 = A.Action('L2', relais2, norm_out=0, pin_ok=relais2_ok, pin_all_ok=led_all_ok,delay = 2, persistent = True)
L3 = A.Action('L3', error_led1, norm_out=0, pin_all_ok=led_all_ok)
L4 = A.Action('L4', error_led2, norm_out=0, pin_all_ok=led_all_ok)
L7 = A.Action('L7', error_led3, norm_out=0, pin_all_ok=led_all_ok)
# L3 = A.Action('L3', led_mcp_analog, norm_out=0, delay = 3, persistent = True)
# L4 = A.Action('L4', led_pico1, norm_out=0)
L5 = A.Action('L5', buzzer_1, norm_out=0, pin_all_ok=led_all_ok, delay = 3, persistent = True)
L6 = A.Action('L6', buzzer_2, norm_out=0, pin_all_ok=led_all_ok, delay = 3, persistent = True)

### SENSORS ###
S1 = A.Sensor('S1', pin_mcp_dig1, 'digital', norm_val=1, actions=[L1, L3, L5])
S2 = A.Sensor('S2', pin_mcp_dig2, 'digital', norm_val=1, actions=[L1, L4, L6])
S3 = A.Sensor('S3', pin_mcp_dig3, 'digital', norm_val=1, actions=[L2, L7])
#S3 = A.Sensor('S3', pin_pico1, 'digital', norm_val=0, actions=[L4])
#S_adc = A.Sensor('S_adc', pin_pico_analog, 'analog', analog_error_threshold, actions=[L3, L6])

set1 = [S1, L1, L5]
set2 = [S2, L1, L6]
set3 = [S3, L2]


# M1 = A.Master('M1', pin_reset_persistent, norm_val=0, mode='reset_selected', object_list=[S1])
M1 = A.Master('M1', pin_reset_persistent, norm_val=0, mode='reset_selected', object_list= [set1, set2, set3])
M2 = A.Master('M2', pin_ignore_sensors, norm_val=0, mode='ignore', object_list=[set1])
# M2 = A.Master('M2', pin_ignore_sensors, norm_val=0, mode='ignore_all')

### TIMER CALLBACK FUNCTION ###
def timer_callback(timer):
    A.reset_action_triggers()
    A.check_sensors()
    A.admin_operation()
    A.run_actions()
    A.check_all_ok()
    # Sleep is NOT needed in this implementation!
    print('time: ', time())
    

### MAIN LOOP ###
# Create a Timer object
timer = Timer(-1)  # Use the first available hardware timer (-1) on the microcontroller

# Set the timer callback function
timer.init(period=20, mode=Timer.PERIODIC, callback=timer_callback)
# The timer will fire every x seconds (x000 milliseconds) and call the 
# timer_callback function.

# No need for a while loop if there are no additional code or operations to run
# while True:
#     pass

# Add any other code or operations you need to perform outside the main loop
