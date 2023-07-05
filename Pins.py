#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:01:32 2023

"""

from machine import Pin, ADC

# Input pins
LC  = Pin(1, Pin.IN)  # Load cell                Normally Closed
# T   = Pin(2, Pin.IN)  # Temperature (Eurotherm)  Normally Closed
# S1B = Pin(4, Pin.IN)  # Sigma 1 bottom           Normally Opened
# S3  = Pin(5, Pin.IN)  # Sigma 3                  Normally Opened
# S1T = Pin(6, Pin.IN)  # Sigma 1 top              Normally Opened
# NOF = Pin(7, Pin.IN)  # Emergency OFF (Notaus)   Normally Closed
# L   = Pin(9, Pin.IN)  # Water leakage            Normally Opened
# WF  = Pin(10, Pin.IN)  # Water flow               Normally Closed
# AOF = Pin(11, Pin.IN)  # All alarms off           Normally Opened

# Output pins
THY   = Pin(14, Pin.OUT)  # Thyristor enabled
MEN   = Pin(15, Pin.OUT)  # Motor enabled
# MOK   = Pin(16, Pin.OUT)  # Motor OK
# WOK   = Pin(17, Pin.OUT)  # Water flow enabled
# ALR   = Pin(19, Pin.OUT)  # Alarm buzzer
# LMC   = Pin(20, Pin.OUT)  # Microcontroller OK
# LPO   = Pin(21, Pin.OUT)  # Motor at top end
# LNO   = Pin(22, Pin.OUT)  # Motor at bottom end

# Alarm indicators
LOF   = Pin(24, Pin.OUT)  # Emergency stop
LT    = Pin(25, Pin.OUT)  # Temperature
# LLC   = Pin(26, Pin.OUT)  # Load cell
# LWF   = Pin(27, Pin.OUT)  # Water flow
# LL    = Pin(29, Pin.OUT)  # Water leakage
# LS1T  = Pin(, Pin.OUT)  # Sigma 1 crash: top
# LS1B  = Pin(, Pin.OUT)  # Sigma 1 crash: bottom
# LS3   = Pin(, Pin.OUT)  # Sigma 3 crash

# Analog input pins
adc0 = ADC(Pin(31))
# adc1 = ADC(Pin(32))
# adc2 = ADC(Pin(34))