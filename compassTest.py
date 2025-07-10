from compass import compassBoard
from machine import I2C, Pin
import time

i2c = I2C(1, scl=Pin(27), sda = Pin(26))
comp = compassBoard(i2c, drdyPin = 14)

if comp.self_test():
    print("Self-test PASSED")
else:
    print("Self-test FAILED")