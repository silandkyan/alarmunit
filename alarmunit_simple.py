#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""

from machine import Pin, ADC
from time import sleep
from Timer import Timer
from Error import Error

# Digital input pins
digital_input_pin = Pin(3, Pin.IN)
digital_output_pin = Pin(4, Pin.OUT)
digital_error_value = 1

# Analog input pins
analog_input_pin = ADC(Pin(26))
analog_output_pin = Pin(5, Pin.OUT)
analog_error_threshold = 5000

# Create instances of Timer and Error
timer = Timer(5)  # Timer with a duration of 5 seconds
digital_error = Error(digital_input_pin, digital_output_pin, digital_error_value)
analog_error = Error(analog_input_pin, analog_output_pin, analog_error_threshold)

# Main program loop
while True:
    if timer.check():  # Check if the timer has expired
        # Check for digital error
        digital_error.check_digital()
        
        # Check for analog error
        analog_error.check_analog()

        # Reset the timer
        timer.reset()
    
    # Add any other code or operations you need to perform within the main loop
    # ...

    # Sleep for a short duration to avoid busy-waiting
    sleep(0.1)
