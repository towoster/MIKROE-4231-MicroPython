from machine import I2C, Pin
import time

# GP17 = SCL, GP16 = SDA → I2C1
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
time.sleep_ms(100)

while True:
    print(i2c.scan())
    time.sleep(1)
