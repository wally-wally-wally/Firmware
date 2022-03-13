import path
import BLE
import BLDC
import camera
import global_vars
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
    global_vars.init()
    wireless = BLE.Socket()
    wally = BLDC.Navigation(PWM_PIN_FR, PWM_PIN_FL, PWM_PIN_BR, PWM_PIN_BL, DIR_PIN_FR, DIR_PIN_FL, DIR_PIN_BR, DIR_PIN_BL, PWM_FREQUENCY, JUMPER)
    cam = camera.Camera()
    route = path.PathManagement(wireless, wally, cam)

    wally.setSpeed(50)

    wireless.advertise()
    wireless.connect()

    return wireless, route

def mainTask():
    wireless, route = init()

    while True:
        data = wireless.read()

        if data.startswith(f'{Commands.START_RECORDING.value}'):
            route.recordPath(data.split(",")[1])
        elif data.startswith(f'{Commands.RUN_TASK.value}'):
            route.executePath(data.split(",")[1])
        elif data == f'{Commands.LIST_TASKS.value}':
            route.listTasks()
