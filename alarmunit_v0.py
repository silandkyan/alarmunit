#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:36:35 2023

"""

##### PINS #####

from machine import Pin

# Input pins
LC  = Pin(3, Pin.IN)  # Load cell                Normally Closed
T   = Pin(4, Pin.IN)  # Temperature (Eurotherm)  Normally Closed
S1B = Pin(5, Pin.IN)  # Sigma 1 bottom           Normally Opened
S3  = Pin(0, Pin.IN)  # Sigma 3                  Normally Opened
S1T = Pin(1, Pin.IN)  # Sigma 1 top              Normally Opened
NOF = Pin(2, Pin.IN)  # Emergency OFF (Notaus)   Normally Closed
L   = Pin(0, Pin.IN)  # Water leakage            Normally Opened
WF  = Pin(1, Pin.IN)  # Water flow               Normally Closed
AOF = Pin(1, Pin.IN)  # All alarms off           Normally Opened

# Output pins
THY   = Pin(7, Pin.OUT)  # Thyristor enabled
MEN   = Pin(6, Pin.OUT)  # Motor enabled
MOK   = Pin(5, Pin.OUT)  # Motor OK
WOK   = Pin(4, Pin.OUT)  # Water flow enabled
ALR   = Pin(3, Pin.OUT)  # Alarm buzzer
LMC   = Pin(4, Pin.OUT)  # Microcontroller OK
LPO   = Pin(5, Pin.OUT)  # Motor at top end
LNO   = Pin(6, Pin.OUT)  # Motor at bottom end

# Alarm indicators
LOF   = Pin(0, Pin.OUT)  # Emergency stop
LT    = Pin(1, Pin.OUT)  # Temperature
LLC   = Pin(2, Pin.OUT)  # Load cell
LWF   = Pin(3, Pin.OUT)  # Water flow
LL    = Pin(4, Pin.OUT)  # Water leakage
LS1T  = Pin(5, Pin.OUT)  # Sigma 1 crash: top
LS1B  = Pin(6, Pin.OUT)  # Sigma 1 crash: bottom
LS3   = Pin(7, Pin.OUT)  # Sigma 3 crash

# Constants
ON  = 1
OFF = 0

WF_FLAG  = 0x01
L_FLAG   = 0x02
S1T_FLAG = 0x04
S1B_FLAG = 0x08
S3_FLAG  = 0x10

# Function declarations
# In Python, you don't need to declare functions in advance, so these are not needed.
# Just define your functions in your Python script.



##### ADC #####

from machine import Pin, ADC

threshold = 2.5

# Create an ADC object
adc = ADC(Pin(26))  # Assuming the analog signal is connected to GPIO 26

# In your main loop, you can read the analog signal like this:
analog_value = adc.read_u16()

# Then you can check if it exceeds the threshold:
if analog_value > threshold:
    # Generate error signal
    pass

    

##### ALARM #####

from machine import Pin
from time import sleep

# Assuming you have the Timer and Check_Timer functions defined elsewhere
# If not, you'll need to implement them in Python
# For now, I'll use sleep as a placeholder

def Timer_3(state):
    global T3_flag
    if state == ON:
        T3_flag = True
    else:
        T3_flag = False

def Timer_5(state):
    sleep(5)

def Check_Timer_3():
    global T3_flag
    return T3_flag

def Check_Timer_5():
    return True

def Timer_1(state):
    sleep(1)

# Global variables
T3_flag = 0x00

# Main program
def main():
    Config()
    Init()
    InitTimers()
    
    while True:
        # All alarms OFF
        if AOF.value() == 1:
            Init()
            T3_flag = 0x00
            Timer_3(OFF)
            Timer_5(OFF)
            while AOF.value() == 1:
                if NOF.value() == 0: break
                if T.value() == 0:   LT.on()
                else:                 LT.off()
                if LC.value() == 0:  LLC.on()
                else:                 LLC.off()
                if WF.value() == 0:  LWF.on()
                else:                 LWF.off()
                if L.value() == 1:   LL.on()
                else:                 LL.off()
                if S1T.value() == 1:
                    LS1T.on()
                    LPO.on()
                else:
                    LS1T.off()
                    LPO.off()
                if S1B.value() == 1:
                    LS1B.on()
                    LNO.on()
                else:
                    LS1B.off()
                    LNO.off()
                if S3.value() == 1:  LS3.on()
                else:                 LS3.off()
            if NOF.value() == 1: Init()

        # Emergency stop or Temperature or Load cell (!NOF, !T, !LC)
        if NOF.value() == 0 or T.value() == 0 or LC.value() == 0:
            if NOF.value() == 0: LOF.on()
            if T.value() == 0:   LT.on()
            if LC.value() == 0:  LLC.on()
            AllOff(ON)

        # Water flow (!WF)
        if WF.value() == 0:
            LWF.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = WF_FLAG
            if T3_flag == WF_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(OFF)
        if WF.value() == 1:
            LWF.off()
            if T3_flag == WF_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Water leakage
        if L.value() == 1:
            LL.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = L_FLAG
            if T3_flag == L_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(OFF)
        if L.value() == 0:
            LL.off()
            if T3_flag == L_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 1 top
        if S1T.value() == 1:
            LS1T.on()
            LPO.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S1T_FLAG
            if T3_flag == S1T_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S1T.value() == 0:
            LS1T.off()
            LPO.off()
            if T3_flag == S1T_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 1 bottom
        if S1B.value() == 1:
            LS1B.on()
            LNO.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S1B_FLAG
            if T3_flag == S1B_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S1B.value() == 0:
            LS1B.off()
            LNO.off()
            if T3_flag == S1B_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

        # Sigma 3
        if S3.value() == 1:
            LS3.on()
            if T3_flag == 0:
                Timer_3(ON)
                T3_flag = S3_FLAG
            if T3_flag == S3_FLAG:
                if Check_Timer_3():
                    Timer_3(OFF)
                    AllOff(ON)
        if S3.value() == 0:
            LS3.off()
            if T3_flag == S3_FLAG:
                Timer_3(OFF)
                T3_flag = 0x00

def Config():
    # Port configuration A[0..2] = analog, all others digital
    # In MicroPython, you can set the mode of a pin (analog or digital) when you create it
    # So this function may not be necessary

    # Port digital I/O configuration
    # In MicroPython, you can set the direction of a pin (input or output) when you create it
    # So this function may not be necessary

    pass

def Init():
    # Output ports: initial values
    # In MicroPython, you can set the initial value of a pin when you create it
    # So this function may not be necessary

    pass

def AllOff(delay):
    Alarm(ON)
    THY.off()
    if delay:
        Timer_5(ON)
        MotorOff()
        while not Check_Timer_5(): pass
        Timer_5(OFF)
        WOK.off()
    else:
        WOK.off()
        MotorOff()
    WaitReset()

def MotorOff():
    MOK.off()
    Timer_1(ON)
    while not Check_Timer_1(): pass
    MEN.off()
    Timer_1(OFF)

def WaitReset():
    LMC.off()
    while True: pass

def Alarm(state):
    if state == ON:
        ALR.on()
        return
    ALR.off()