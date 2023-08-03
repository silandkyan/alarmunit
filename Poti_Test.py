# Poti Test 

from machine import Pin, ADC            #importing Pin and ADC class
from time import sleep                  #importing sleep class
potentiometer = ADC(26)           #creating potentiometer object

while True:
        potentiometer_value = potentiometer.read_u16()   #reading analog pin
        print(potentiometer_value)                   #printing the ADC value
        sleep(0.25)