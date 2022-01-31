#this is not meant to be in the main code
#each cell has the same i2c fuel gauge and therefore
#the address needs to be changed so we can communicate with
#each cell simultaneously (it's a programmable address IC)
#this only needs to run once ever and the addresses are stored in EEPROM
#create a main.py, create object, and then run rebalance()

import GPIO
import i2c
import BMS
import time

class Cell:
    def __init__(self, cell1_EN, cell2_EN, cell3_EN, cell4_EN, i2c_channel):
        self.cells = [cell1_EN, cell2_EN, cell3_EN, cell4_EN]
        self.i2c = i2c.I2C(i2c_channel)

        GPIO.init()
        for x in self.cells:
            GPIO.setPin(x, 'OUT', 'NONE')
            GPIO.write(x, 'LOW')

    def rebalance(self):
        count = 0
        for x in self.cells:
            GPIO.write(x, 'HIGH')
            time.sleep(1000)

            setAddress(BMS.cell_addr[count])
            time.sleep(1000)

            GPIO.write(x, 'LOW')
            time.sleep(1000)
            count+=1

    def setAddress(self, address):
        data = self.i2c.read(BMS.base_addr, BMS.special_reg)
        self.i2c.write(BMS.base_addr, BMS.special_reg, (data | 1<<2))	#set 2nd bit to 1 (enable write)

        self.i2c.write(BMS.base_addr, BMS.EEPROM_reg, address)          #set address
        self.i2c.write(address, BMS.memory_reg, 0x44)                   #store address in EEPROM

        data = self.i2c.read(address, BMS.special_reg)
        self.i2c.write(address, BMS.special_reg, (data & ~(1<<2)))      #set 2nd bit back to 0 (disable write)
