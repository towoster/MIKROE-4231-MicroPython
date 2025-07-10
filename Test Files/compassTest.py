from compass import compassBoard
from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda = Pin(0), freq=100000)
comp = compassBoard(i2c, drdyPin = 14)

time.sleep(0.1)

if comp.selfTest():
    print("Self-test PASSED")
else:
    print("Self-test FAILED")