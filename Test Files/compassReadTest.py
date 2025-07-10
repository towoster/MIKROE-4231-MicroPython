from machine import I2C, Pin
import time
from compass import compassBoard

i2c = I2C(0, scl=Pin(1), sda = Pin(0), freq=100000)
comp = compassBoard(i2c, drdyPin = 14)

while True:
    data = comp.read()
    uTeslas = dict( x = data['x'] * 0.15, y = data['y'] * 0.15, z = data['z'] * 0.15 )
    #print("X: {:5d} | Y: {:5d} | Z: {:5d}".format(data['x'], data['y'], data['z']))
    print("X: {:5f} | Y: {:5f} | Z: {:5f}".format(uTeslas['x'], uTeslas['y'], uTeslas['z']))
    time.sleep(0.2)