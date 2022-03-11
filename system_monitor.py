import threading
import time
import global_vars
#import BMS

from uart import UART
import i2c
import lidar

# Event set if Lidar detects object
#CollisionDetected = False
#CollisionEvent = threading.Event()

I2c = None
Charger = None
Cells = [None] * 4

DIST_THRESH = 800 # mm

# Should be defined in BMS
NUM_CELLS = 4
MAX_VOLT_THRESH = 4.2
MIN_VOLT_THRESH = 4.158 # 2 * 0.99
DISCHARGE_TOL = 1.01 # 1% Tolerance

# Array of bools for each degree; True if an object is within DIST_THRESH
lidarData = [False] * 360

def init():

    global Uart
    global Lidar
    Uart = UART(lidar.PORT, lidar.BAUD)
    Lidar = lidar.Lidar(Uart)
    global obstruction
    obstruction = False
    print(Lidar)
    #I2c = i2c.I2C(i2c.MAIN_CHANNEL)
    #Charger = BMS.Charger(I2c)
    #for i in range(BMS.NUM_CELLS)
        #Cells[i] = BMS.Cell(i, enPin[i], I2c)

def getAnglesFromDirection():
    return 45, 135
    if global_vars.WallyDirection == 'F':
        return -45, 45
    elif global_vars.WallyDirection == 'R':
        return 45, 135
    elif global_vars.WallyDirection == 'B':
        return 135, 225
    elif global_vars.WallyDirection == 'L':
        return 225, 315

def inRange(ang, angL, angU):
    if angL > 0:
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

def sysMon():
    init()
    #print(Lidar)
    #print(obstruction)

    while True:
        #time.sleep(1.5)
        Lidar.readData()
        Lidar.dataCorrection()

        CollisionDetection()

if __name__ == '__main__':
    global_vars.init()
    sysMon()

