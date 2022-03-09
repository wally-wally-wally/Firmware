import path
import BLE
import BLDC
#import camera
from commands import Commands

PWM_PIN_FR = 10
PWM_PIN_FL = 17
PWM_PIN_BR = 17
PWM_PIN_BL = 10
DIR_PIN_FR = 22
DIR_PIN_FL = 4
DIR_PIN_BR = 27
DIR_PIN_BL = 9
PWM_FREQUENCY = 20000
JUMPER = True

def init():
    wireless = BLE.Socket()
    wally = BLDC.Navigation(PWM_PIN_FR, PWM_PIN_FL, PWM_PIN_BR, PWM_PIN_BL, DIR_PIN_FR, DIR_PIN_FL, DIR_PIN_BR, DIR_PIN_BL, PWM_FREQUENCY, JUMPER)
    #cam = camera.Camera()
    route = path.PathManagement(wireless, wally)

    wally.setSpeed(50)

    wireless.advertise()
    wireless.connect()

    return wireless, route

def mainTask():
    wireless, route = init()

    while True:
        data = wireless.read()

        if data.startswith(Commands.START_RECORDING):
            print ("recording")
            route.recordPath(data.split(",")[1])
        elif data.startswith(Commands.RUN_TASK):
            print ("execute")
            route.executePath(data.split(",")[1])
        elif data == f'{Commands.LIST_TASKS.value}':
            route.listTasks()
