import i2c
import mux

ENCODER_ADDR = 0x36
ANG_REG = 0xE
ANG_MASK = 0xFFF

# Ang Range: 0 - FFF

class Encoder():
    def __init__(self, i2c):
        self.i2c = i2c

    def getAng():
        data = self.i2c.read_word(ENCODER_ADDR, ANG_REG)
        data = ((data & 0xFF) << 8) | (data >> 8)
        # Convert to deg
        data = data * (360 / 0xFFF)
        return data

    def __del__():
        pass

class MotorPosition(self):
    def __init__(self, i2c)
        self.encoder = Encoder(i2c)
        self.mux = Mux(i2c)

    def getAngles(self):
        angles = []
        for i in range(mux.CHAN0_EN, mux.CHAN3_EN + 1)
            self.mux.enableChannel(i)
            angles.append(self.encoder.getAng())
        return angles

    def __del__():
        pass

