from machine import I2C, Pin
import time, struct

class compassBoard:
    def __init__(self, i2c, addr = 0x0C, drdyPin: int = None):
        self.i2c, self.addr = i2c, addr
        if drdyPin is not None:
            self.drdy = Pin(drdyPin, Pin.IN)
        else:
            self.drdy = None
        
        #Check correct manufacturer ID
        if self._read_u8(0x00) != 0x48:
            raise RuntimeError("Compass not detected")
        
        #Soft reset - writing 01 to CNTL3 reg
        self._write_u8(0x32, 0x01)
        time.sleep_ms(10)
        
        #Enter power down, required for config - write 00 to CNTL2
        self._write_u8(0x31, 0x00)
        time.sleep_ms(10)
        
        #Set mode to continuous measurement at 1Hz
        #   1Hz - 0C
        #  10Hz - 02
        #  20Hz - 04
        #  50Hz - 06
        # 100Hz - 08
        # 200Hz - 0A
        self._write_u8(0x31, 0x0C)
        time.sleep_ms(10)
        
    #Function for reading from compass registers
    def _read_u8(self, reg):
        return int.from_bytes(self.i2c.readfrom_mem(self.addr, reg, 1), 'little')
    
    #Function for writing to compass registers
    def _write_u8(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))
        
    def read(self) -> dict:
        while (!(self.drdy)):
            time.sleep_ms(2)
            
        raw = self.i2c.readfrom_mem(self.addr, 0x11, 6)
        x, y, z = struct.unpack('<hhh', raw)
        
        st2 = self._read_u8(0x18)
        if st2 & 0x08:
            raise RuntimeError("Magnetometer overflow")
        if st2 & 0x04:
            raise RuntimeError("Invalid magnetometer data")
        
        return {'x':x, 'y':y, 'z':z}
    
    def selfTest(self):
        # Power down mode
        self._write_u8(0x31, 0x00)
        time.sleep_ms(10)
        
        # Enter self test
        self._write_u8(0x31, 0x10)
        time.sleep_ms(10)
        
        for _ in range(20):
            if drdy:
                break
            time.sleep_ms(5)
        else:
            raise RuntimeError("Self-test timed out waiting for data ready")
        
        raw = self.i2c.readfrom_mem(self.addr, 0x11, 6)
        x, y, z = struct.unpack('<hhh', raw)
        
        self._write_u8(0x31, 0x00)
        
        return (200 <= z <= 600)
        
        