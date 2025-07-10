from machine import I2C, Pin
import time

# GP17 = SCL, GP16 = SDA → I2C1
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
time.sleep_ms(100)

while True:
    print(i2c.scan())
    time.sleep(1)
