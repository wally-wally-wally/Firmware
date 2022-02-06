import GPIO
import i2c
import time

#Cell Addresses
cellAddr = [0x34, 0x35, 0x36, 0x37]

#DS2782 Addresses
GAUGE_BASE_ADDR = 0x34
SPECIAL_REG = 0x15
EEPROM_REG = 0x7E
MEMORY_REG = 0xFE
VOLT_REG_MSB = 0x0C
VOLT_REG_LSB = 0x0D
MAX_VOLT = 4.2
MIN_VOLT = 3.3

#BQ24179 Addresses
CHG_BASE_ADDR = 0x6B
CHG_CTRL = 0xF
CHG_STAT = 0x1C

#charger status
CHARGING = int('011', 2)
DONE_CHARGING = int('111', 2)

class Cell:
    def __init__(self, cellNum, enPin, i2cChannel):
        self.enPin = enPin
        self.i2c = i2c.I2C(i2cChannel)
        self.address = cellAddr[cellNum-1]
        self.isDischarging = False

        GPIO.init()
        GPIO.setPin(self.enPin, 'OUT', 'NONE')
        GPIO.write(self.enPin, 'HIGH')

    def readVoltage(self):                              #might need to be converted to an understandable value
        return self.i2c.read(self.address, VOLT_REG_MSB)

    def dischargeCell(self):
        data = self.i2c.read(self.address, SPECIAL_REG)
        self.i2c.write(self.address, SPECIAL_REG, (data & ~(1<<1))) #set PIO to low power mode
        self.isDischarging = True
        return self.isDischarging

    def stopDischarge(self):
        data = self.i2c.read(self.address, SPECIAL_REG)
        self.i2c.write(self.address, SPECIAL_REG, (data | 1<<1))   #set PIO back to normal mode
        self.isDischarging = False
        return self.isDischarging

class Charger:
    def __init__(self, cePin, qonPin, i2cChannel):
        self.i2c = i2c.I2C(i2cChannel)
        self.cePin = cePin
        self.qonPin = qonPin
        self.isCharging = False

        GPIO.init()
        GPIO.setPin(self.cePin, 'OUT', 'NONE')
        GPIO.setPin(self.qonPin, 'OUT', 'NONE')
        GPIO.write(self.qonPin, 'HIGH')
        enableCharging()

    def reset(self):
        GPIO.write(self.qonPin, 'LOW')
        time.sleep(10)

    def disableDevices(self, *pins):                   #disable high current devices for charging
        for x in pins:
            GPIO.write(x, 'LOW')

    def enableDevices(self, *pins):                    #re-enable high current devices when done charging
        for x in pins:
            GPIO.write(x, 'HIGH')

    def enableCharging(self):
        GPIO.write(self.cePin, 'LOW')
        data = self.i2c.read(CHG_BASE_ADDR, CHG_CTRL)
        self.i2c.write(CHG_BASE_ADDR, CHG_CTRL, (data | 1<<5))

    def disableCharging(self):
        GPIO.write(self.cePin, 'HIGH')
        data = self.i2c.read(CHG_BASE_ADDR, CHG_CTRL)
        self.i2c.write(CHG_BASE_ADDR, CHG_CTRL, (data & ~(1<<5)))

    def checkChargeStatus(self):                       #can be modified to include the other states
        data = readStatus()
        if int(data) == CHARGING:
            self.isCharging = True
        else:
            self.isCharging = False

    def readStatus(self):
        data = int(self.i2c.read(CHG_BASE_ADDR, CHG_STAT), 2)
        mask = int('00000111', 2)

        return bin(data & mask)