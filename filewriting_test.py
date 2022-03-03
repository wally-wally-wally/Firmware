import path
import time
import BLE

wireless = BLE.Socket()
wireless.advertise()
wireless.connect()

pathFile = path.Path("MyFile", wireless)

pathFile.recordPath()
pathFile.reversePath()
