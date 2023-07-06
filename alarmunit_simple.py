#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""

from machine import Pin, ADC, Timer
from Error import Error

# Digital pins
digital_input_pin = Pin(3, Pin.IN)
digital_error_pin = Pin(4, Pin.OUT)
digital_error_value = 1
analog_error_pin = Pin(5, Pin.OUT)
no_errors_pin = Pin(6, Pin.OUT)

# Analog input pins
analog_input_pin = ADC(Pin(26))
analog_error_threshold = 5000

# Create instances Error class
digital_error = Error(digital_input_pin, digital_error_pin, digital_error_value)
analog_error = Error(analog_input_pin, analog_error_pin, analog_error_threshold)

# Timer callback function
def timer_callback(timer):
    # Check for digital error
    digital_error.check_digital()

    # Check for analog error
    analog_error.check_analog()
    
    # Check for no errors and light pin
    Error.handle_no_errors(no_errors_pin)
    
    # Sleep is NOT needed in this implementation!

# Create a Timer object
timer = Timer(-1)  # Use the first available hardware timer (-1) on the microcontroller

# Set the timer callback function
timer.init(period=5000, mode=Timer.PERIODIC, callback=timer_callback)
# The timer will fire every 5 seconds (5000 milliseconds) and call the 
# timer_callback function. Within these periods, not other code is executed.

# No need for a while loop if there are no additional code or operations to run
# while True:
#     pass

# Add any other code or operations you need to perform outside the main loop
