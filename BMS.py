import GPIO
import i2c

#Cell Addresses
cell_addr = [0x34, 0x35, 0x36, 0x37]

#DS2782 Addresses
base_addr = 0x34
special_reg = 0x15
EEPROM_reg = 0x7E
memory_reg = 0xFE
volt_reg_msb = 0x0C
volt_reg_lsb = 0x0D

#BQ24179 Addresses
chg_base_addr = 0x6B
chg_ctrl = 0xF
chg_stat = 0x1C

#charger status
charging = int('011', 2)
done_charging = int('111', 2)

class Cell:
    def __init__(self, cell_num, EN_PIN, i2c_channel):
        self.en_pin = EN_PIN
        self.i2c = i2c.I2C(i2c_channel)
        self.address = cell_addr[cell_num-1]
        self.isDischarging = False

        GPIO.init()
        GPIO.setPin(self.en_pin, 'OUT', 'NONE')
        GPIO.write(self.en_pin, 'HIGH')

    def readVoltage(self):                              #might need to be converted to an understandable value
        return self.i2c.read(self.address, volt_reg_msb)

    def dischargeCell(self):
        data = self.i2c.read(self.address, special_reg)
        self.i2c.write(self.address, special_reg, (data & ~(1<<1))) #set PIO to low power mode
        self.isDischarging = True
        return self.isDischarging

    def stopDischarge(self):
        data = self.i2c.read(self.address, special_reg)
        self.i2c.write(self.address, special_reg, (data | 1<<1))   #set PIO back to normal mode
        self.isDischarging = False
        return self.isDischarging

class Charger:
    def __init__(self, stat_pin, CE_pin, i2c_channel):
        self.i2c = i2c.I2C(i2c_channel)
        self.CE_pin = CE_PIN
        self.stat_pin = stat_pin
        self.isCharging = False

        GPIO.init()
        GPIO.setPin(self.en_pin, 'OUT', 'NONE')
        enableCharging()

    def disableDevices(self, *pins):                   #disable high current devices for charging
        for x in pins:
            GPIO.write(x, 'LOW')

    def enableDevices(self, *pins):                    #re-enable high current devices when done charging
        for x in pins:
            GPIO.write(x, 'HIGH')

    def enableCharging(self):
        GPIO.write(self.CE_pin, 'LOW')
        data = self.i2c.read(chg_base_addr, chg_ctrl)
        self.i2c.write(chg_base_addr, chg_ctrl, (data | 1<<5))

    def disableCharging(self):
        GPIO.write(self.CE_pin, 'HIGH')
        data = self.i2c.read(chg_base_addr, chg_ctrl)
        self.i2c.write(chg_base_addr, chg_ctrl, (data & ~(1<<5)))

    def checkChargeStatus(self):                       #can be modified to include the other states
        data = readStatus()
    if int(data) == charging:
        self.isCharging = True
    else:
        self.isCharging = False

    def readStatus(self):
        data = int(self.i2c.read(chg_base_addr, chg_stat), 2)
        mask = int('00000111', 2)

        return bin(data & mask)