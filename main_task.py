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
    route = path.PathManagement(wireless, wally)

    wally.setSpeed(50)

    wireless.advertise()
    wireless.connect()

    return wireless, route

def mainTask():
    wireless, route = init()

    while True:
        data = wireless.read()

        if data == f'{Commands.START_RECORDING.value}'.encode():
            pathName = wireless.read()
            route.recordPath(pathName.decode())
        elif data == f'{Commands.RUN_TASK.value}'.encode():
            pathName = wireless.read()
            route.executePath(pathName.decode())
        elif data == f'{Commands.LIST_TASKS.value}'.encode():
            route.listTasks()
