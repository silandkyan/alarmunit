 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:15 2023

@author: pgross
"""

from machine import Pin, ADC, Timer
from Error_test import Error


# Digital pins
digital_input_pin_1 = Pin(22, Pin.IN)
digital_error_pin_1 = Pin(17, Pin.OUT)
digital_error_value_1 = 1

#digital_input_pin_2 = Pin(20, Pin.IN)
#digital_error_pin_2 = Pin(18, Pin.OUT)
#digital_error_value_2 = 0

analog_error_pin_1 = Pin(18, Pin.OUT)
no_errors_pin = Pin(16, Pin.OUT)

# Analog input pins
analog_input_pin_1 = ADC(Pin(26))
#analog_input_pin_2 = ADC(Pin(27))
analog_error_threshold = 32000

# Create instances Error class
digital_error_1 = Error(digital_input_pin_1, digital_error_pin_1, digital_error_value_1)
#digital_error_2 = Error(digital_input_pin_2, digital_error_pin_2, digital_error_value_2)
analog_error_1 = Error(analog_input_pin_1, analog_error_pin_1, analog_error_threshold)


# Timer callback function
def timer_callback(timer):
    # Check for digital error
    digital_error_1.check_digital()
    #digital_error_2.check_digital()

    # Check for analog error
    analog_error_1.check_analog()
    
    # Check for no errors and light pin
    Error.handle_no_errors(no_errors_pin)
    
    # Sleep is NOT needed in this implementation!

# Create a Timer object
timer = Timer(-1)  # Use the first available hardware timer (-1) on the microcontroller

# Set the timer callback function
timer.init(period=2000, mode=Timer.PERIODIC, callback=timer_callback)
# The timer will fire every 5 seconds (5000 milliseconds) and call the 
# timer_callback function. Within these periods, not other code is executed.

# No need for a while loop if there are no additional code or operations to run
# while True:
#     pass

# Add any other code or operations you need to perform outside the main loop
