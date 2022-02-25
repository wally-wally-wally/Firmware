# I2C controlled mux
import i2c

# Address is configurable by HW; all toggle pins pulled to GND
ADDR = 0x70

CHAN_DIS = 0x00
CHAN0_EN = 0x04
CHAN1_EN = 0x05
CHAN2_EN = 0x06
CHAN3_EN = 0x07

class Mux():
    def __init__(self, i2c):
       self.i2c = i2c 

    def enableChannel(self, channel):
        self.i2c.write_byte(ADDR, channel)

