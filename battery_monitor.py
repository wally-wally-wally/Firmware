import i2c
import time
import global_vars
import GPIO

GAUGE_BASE_ADDR = 0x34
VOLT_REG_MSB = 0x0C
CELL_GPIO_EN = [12, 16, 20, 21]
NUM_CELLS = 4
MIN_VOLTAGE = 3.7

def readCellVoltages(I2c):
    voltages = [0] * 4
    for i in range(NUM_CELLS):
        GPIO.write(CELL_GPIO_EN[i], 'HIGH')
        time.sleep(0.1)
        rawData = I2c.read_word(GAUGE_BASE_ADDR, VOLT_REG_MSB)
        rawData = rawData << 8 & 0xFF00 | rawData >> 8
        rawData >>= 5
        voltages[i] = rawData * 4.88
        time.sleep(0.1)
        GPIO.write(CELL_GPIO_EN[i], 'LOW')
        
    return voltages

# NANANANANANANANANNANA batMon
def batMon():
   GPIO.init()
   I2c = i2c.I2C(1)
   for i in CELL_GPIO_EN:
       GPIO.setPin(i, 'OUT', 'NONE')
   while (True):
       voltages = readCellVoltages(I2c)
       for voltage in voltages:
           if voltage < MIN_VOLTAGE: 
               global_vars.LowBattDetected = True

       time.sleep(60)

if __name__ == '__main__':
    global_vars.init()
    batMon()
