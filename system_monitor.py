import threading
import time
#import BMS

from uart import UART
import i2c
import lidar

# Event set if Lidar detects object
CollisionEvent = threading.Event()

Lidar = None
Uart = None
I2c = None
Charger = None
Cells = [None] * 4

DIST_THRESH = 100 # mm

# Should be defined in BMS
NUM_CELLS = 4
MAX_VOLT_THRESH = 4.2
MIN_VOLT_THRESH = 4.158 # 2 * 0.99
DISCHARGE_TOL = 1.01 # 1% Tolerance

def init():
    Uart = UART(lidar.PORT, lidar.BAUD)
    Lidar = lidar.Lidar(Uart)
    #I2c = i2c.I2C(i2c.MAIN_CHANNEL)
    #Charger = BMS.Charger(I2c)
    #for i in range(BMS.NUM_CELLS)
        #Cells[i] = BMS.Cell(i, enPin[i], I2c)


def sysMon():
    init()

    while True:
        Lidar.readData()
        Lidar.dataCorrection()

        # Checks if object is close; does not check angle/relative to movement
        for i in range(Lidar.dist.size()):
            if Lidar.dist[i] < DIST_THRESH:
                CollisionEvent.set()
        
        dischargingCells = False
        Charger.checkChargeStatus()
        
        if Charger.isCharging is False:
            voltage = [0] * 4
            for i in range(NUM_CELLS):
                voltage[i] = Cells[i].readVoltage()

            maxVoltage = max(voltage)
            minVoltage = min(voltage)
            minIndex = voltage.index(minVoltage)
            if maxVoltage >= MAX_VOLT_THRESH and minVoltage >= MIN_VOLT_THRESH:
                Charger.enableDevices()
            elif maxVoltage >= MAX_VOLT_THRESH:
                dischargingCells = True
                Charger.disableCharging()
                for i in range(NUM_CELLS):
                    if i != minIndex:
                        Cells[i].dischargeCell()

        elif Charger.isCharging is True and dischargingCells is True:
            allCellsDischarged = True
            voltage = [0] * 4
            for i in range(NUM_CELLS):
                voltage[i] = Cells[i].readVoltage()
                if voltage[i] <= (min(voltage) * DISCHARGE_TOL):
                    Cells[i].stopDischarge()
                if Cells[i].isDischarging is True:
                    allCellsDischarged = False

            if allCellsDischarged is True:
                Charger.enableCharging()
                dischargingCells = False



                


            
            


#if readStatus() 

#    while(isCharging): 

#        if readStatus() == done_charging 

#            readVoltage (at all cells) 

#            find max voltage 

#            find min voltage and store address of min 

#            if max >= 4.2 and min >=4.158 

#                enableDevices 

#                isCharging = False 

#            else if max >= 4.2 

#                disableCharging 

#                discharge all cells except min cell 

#                while(cells are discharging) 

#                    read voltage 

#                    if voltage > 0.99(min) 

#                        stopDischarge 

#                    if isDischarging == false for all cells 

#                         cells are discharging = false 

#                enableCharging 