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

DIST_THRESH = 100 # mm

def init():
    Uart = UART(lidar.PORT, lidar.BAUD)
    Lidar = lidar.Lidar(Uart)
    #I2c = i2c.I2C(i2c.MAIN_CHANNEL)
    #Charger = BMS.Charger(I2c)


def sysMon():
    init()

    while True:
        Lidar.readData()
        Lidar.dataCorrection()

        # Checks if object is close; does not check angle/relative to movement
        for i in range(Lidar.dist.size()):
            if Lidar.dist[i] < DIST_THRESH:
                CollisionEvent.set()

        