from machine import Pin, Timer
from utime import sleep

Pin = Pin(25, Pin.OUT)

def timer_callback(timer):
    Pin.on()
    sleep(1)
    Pin.off()

timer = Timer(-1)

timer = timer.init(period=5000, mode=Timer.PERIODIC, callback=timer_callback)