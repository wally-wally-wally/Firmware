import path
import BLE
import BLDC
import time

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

    wireless.advertise()
    wireless.connect()

def mainTask():
    init()
    
    while True:                 #BLE data received to be determined by app
        data = wireless.read()
        if data == 'record':
            pathName = wireless.read()
            
            
