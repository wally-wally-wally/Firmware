import threading
import time
import global_vars
#import GPIO
#import BMS

from uart import UART
import i2c
import lidar

# Event set if Lidar detects object
#CollisionDetected = False
#CollisionEvent = threading.Event()

#I2c = None
#Charger = None
Cells = [None] * 4

DIST_THRESH = 1000 # mm

# Should be defined in BMS
NUM_CELLS = 4
MAX_VOLT_THRESH = 4.2
MIN_VOLT_THRESH = 3.2#4.158 # 2 * 0.99
DISCHARGE_TOL = 1.01 # 1% Tolerance

# Array of bools for each degree; True if an object is within DIST_THRESH
lidarData = [False] * 360

def init():

    global Uart
    global Lidar
    global I2c
    Uart = UART(lidar.PORT, lidar.BAUD)
    Lidar = lidar.Lidar(Uart)
#    I2c = i2c.I2C(1)
    global obstruction
    obstruction = False
#    GPIO.init()
#    for i in range(NUM_CELLS):
#        GPIO.setPin(CELL_GPIO_EN[i], 'OUT', 'NONE')
    #print(Lidar)
    #I2c = i2c.I2C(i2c.MAIN_CHANNEL)
    #Charger = BMS.Charger(I2c)
    #for i in 
    # range(BMS.NUM_CELLS)
        #Cells[i] = BMS.Cell(i, enPin[i], I2c)

def getAnglesFromDirection():
    if global_vars.WallyDirection == 'B':
        return -40, 40
    elif global_vars.WallyDirection == 'L':
        return 50, 130
    elif global_vars.WallyDirection == 'F':
        return 140, 220
    elif global_vars.WallyDirection == 'R':
        return 230, 310
    elif global_vars.WallyDirection == 'N':
        return 0, 0


def inRange(ang, angL, angU):
    if angL >= 0:
        return ang > angL and ang < angU
    else:
        return (ang > (angL + 360) and ang <= 360) or (ang < angU and ang >= 0)


def CollisionDetection():
    global obstruction

    angL, angU = getAnglesFromDirection()

    for i in range(len(Lidar.dist)):
        #print(str(l.ang[i]) + ": " + str(l.dist[i]))
        if Lidar.ang[i] == 0:
            continue
        rounded = round(Lidar.ang[i])
        if rounded >= 360:
            rounded = rounded - 360
        if inRange(Lidar.ang[i], angL, angU):
            if Lidar.dist[i] < DIST_THRESH and Lidar.dist[i] != 0:
                #if(data[rounded] is True):
                if obstruction is False:
                    print('New obstruction', flush = True)
                    global_vars.CollisionDetected = True
                    #CollisionEvent.set()
                obstruction = True
                lidarData[rounded] = True

            else:
                lidarData[rounded] = False

    old = obstruction
    obstruction = False
    for i in range(angL, angU):
        if lidarData[i] is True:
            obstruction = True
            break
    if obstruction is False and old is True:
        print ('Obstruction Removed', flush = True)  
        global_vars.CollisionDetected = False
        #CollisionEvent.clear()


# Not Currently in use/tested
def CellRebalance():
    dischargingCells = False
        
    #if Charger.isCharging is False:
    voltage = [0] * 4
    for i in range(NUM_CELLS):
        voltage[i] = Cells[i].readVoltage()

    maxVoltage = max(voltage)
    minVoltage = min(voltage)
    minIndex = voltage.index(minVoltage)
    #if maxVoltage >= MAX_VOLT_THRESH and minVoltage >= MIN_VOLT_THRESH:
    #   Charger.enableDevices()
    if (maxVoltage >= MAX_VOLT_THRESH) or (maxVoltage > minVoltage * DISCHARGE_TOL):
        dischargingCells = True
    #    Charger.disableCharging()
        for i in range(NUM_CELLS):
            if i != minIndex:
                Cells[i].dischargeCell()

    #elif Charger.isCharging is True and dischargingCells is True:
    allCellsDischarged = True
    while allCellsDischarged is True:
        voltage = [0] * 4
        for i in range(NUM_CELLS):
            voltage[i] = Cells[i].readVoltage()
            if voltage[i] <= (min(voltage) * DISCHARGE_TOL) and (voltage[i] < MAX_VOLT_THRESH):
                Cells[i].stopDischarge()
            if Cells[i].isDischarging is True:
                allCellsDischarged = False
        
        #time.sleep(0.5)

def sysMon():
    init()
#    print('sysmon', flush=True)
    #print(Lidar)
    #print(obstruction)
    #CellRebalance()

    while True:
        #time.sleep(1.5)
        Lidar.readData()
        Lidar.dataCorrection()

        CollisionDetection()

        #CellMonitor()

if __name__ == '__main__':
    global_vars.init()
    init()
    while True:
        print(readCellVoltages())        
        time.sleep(1)
    #sysMon()

