#this is not meant to be in the main code
#each cell has the same i2c fuel gauge and therefore
#the address needs to be changed so we can communicate with
#each cell simultaneously (it's a programmable address IC)
#this only needs to run once ever and the addresses are stored in EEPROM
#create a main.py, create object, and then run programAddress()

import GPIO
import i2c
import BMS
import time

class CellAddress:
    def __init__(self, cell1EN, cell2EN, cell3EN, cell4EN, i2cChannel):
        self.cells = [cell1EN, cell2EN, cell3EN, cell4EN]
        self.i2c = i2c.I2C(i2Channel)

        GPIO.init()
        for x in self.cells:
            GPIO.setPin(x, 'OUT', 'NONE')
            GPIO.write(x, 'LOW')

    def setAddress(self):
        count = 0
        for x in self.cells:
            GPIO.write(x, 'HIGH')
            time.sleep(0.5)

            setCellAddress(BMS.cellAddr[count])
            time.sleep(0.5)

            GPIO.write(x, 'LOW')
            time.sleep(0.5)
            count+=1

    def setCellAddress(self, address):
        data = self.i2c.read(BMS.GAUGE_BASE_ADDR, BMS.SPECIAL_REG)
        self.i2c.write(BMS.GAUGE_BASE_ADDR, BMS.SPECIAL_REG, (data | 1<<2))	#set 2nd bit to 1 (enable write)

        self.i2c.write(BMS.GAUGE_BASE_ADDR, BMS.EEPROM_REG, address)          #set address
        self.i2c.write(address, BMS.MEMORY_REG, 0x44)                   #store address in EEPROM

        data = self.i2c.read(address, BMS.SPECIAL_REG)
        self.i2c.write(address, BMS.SPECIAL_REG, (data & ~(1<<2)))      #set 2nd bit back to 0 (disable write)
