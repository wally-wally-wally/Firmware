import path
import BLE
import BLDC
from commands import Commands

PWM_PIN_FR =
PWM_PIN_FL =
PWM_PIN_BR =
PWM_PIN_BL =
DIR_PIN_FR =
DIR_PIN_FL =
DIR_PIN_BR =
DIR_PIN_BL =
PWM_FREQUENCY = 20000

def init():
    wireless = BLE.Socket()
    wally = BLDC.Navigation(PWM_PIN_FR, PWM_PIN_FL, PWM_PIN_BR, PWM_PIN_BL, DIR_PIN_FR, DIR_PIN_FL, DIR_PIN_BR, DIR_PIN_BL, PWM_FREQUENCY)
    path = path.PathManagement(wireless, wally)

    wireless.advertise()
    wireless.connect()

def mainTask():
    init()
    
    while True:                         #BLE data received determined by app - TBD
        data = wireless.read()
        if data == b'Commands.START_RECORDING':
            pathName = wireless.read()  #pathName might need to be converted depending on how we're receiving BLE data
            path.recordPath(str(pathName))
        elif data == b'Commands.RUN_TASK':
            pathName = wireless.read()
            path.executePath(str(pathName))
