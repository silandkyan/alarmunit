#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 14:31:36 2023

@author: pgross
"""

import machine
sda=machine.Pin(12)
scl=machine.Pin(13)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))