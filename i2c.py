import smbus


class I2C():
    # Channel: I2C channel; 0 or 1
    def __init__(self, channel):
        self.bus = smbus.SMBus.(channel)

    # Addr: Address, Reg: Register, val: array of 32 bit values to write
    def write(self, addr, reg, val[]):
        self.bus.write_block_data(addr, reg, val)

    def read(self, addr, reg):
        return self.bus.read_block_data(addr, reg)
