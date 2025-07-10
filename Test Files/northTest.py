from machine import I2C, Pin
import time
from compass import compassBoard
import math

i2c = I2C(0, scl=Pin(1), sda = Pin(0), freq=100000)
comp = compassBoard(i2c, drdyPin = 14)

while True:
    data = comp.read()
    mx = data['x']
    my = data['y']
    heading_rad = math.atan2(my, mx)
    heading_deg = math.degrees(heading_rad)
    heading_deg -= 90
    if heading_deg < 0:
        heading_deg += 360
    elif heading_deg >= 360:
        heading_deg -=360
    print(heading_deg)