import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)          #use broadcom pin numbers (label on pins not physical pin number)
    GPIO.setwarnings(True)

def setPin(pin, direction, PUD):
    if PUD == 'NONE':
        GPIO.setup(pin, setDirection(direction))
    else:
        GPIO.setup(pin, setDirection(direction), pull_up_down = setPUD(PUD))

def setDirection(direction):        #not meant to be used outside this module
    if direction == 'OUT':
        return GPIO.OUT
    elif direction == 'IN':
        return GPIO.IN
    else:
        print ("Error in direction declaration, expected either: 'IN' or 'OUT'")
        return

def setPUD(PUD):                    #not meant to be used outside this module
    if PUD == 'UP':
        return GPIO.PUD_UP
    elif PUD == 'DOWN':
        return GPIO.PUD_DOWN
    else:
        print ("Error in PUD declaration, expected either: 'NONE', 'UP', or 'DOWN'")
        return

def write(pin, output):
    if output == 'HIGH':
        GPIO.output(pin, GPIO.HIGH)
    elif output == 'LOW':
        GPIO.output(pin, GPIO.LOW)
    else:
        GPIO.output(pin, output)    #values accepted are 1, 0, True, False - RPi.GPIO will send an error if it isn't

def read(pin):                      #returns data read at pin - 1 or 0
    return GPIO.input(pin)

def closeGPIO():
    GPIO.cleanup()
