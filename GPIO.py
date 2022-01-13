import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)    #use broadcom pin numbers (label on pins not physical pin number)

def setPin(pin, direction, PUD):
    if PUD == 'NONE':
        GPIO.setup(pin, setDirection(direction))
    else:
        GPIO.setup(pin, setDirection(direction), pull_up_down = setPUD(PUD))

def setDirection(direction):  #not meant to be used outside this module
    if direction == 'OUT':
        return GPIO.OUT
    elif direction == 'IN':
        return GPIO.IN
    else:
        print ("Error in direction declaration, expected either: 'IN' or 'OUT'")
        return

def setPUD(PUD):              #not meant to be used outside this module
    if PUD == 'UP':
        return GPIO.PUD_UP
    elif PUD == 'DOWN':
        return GPIO.PUD_DOWN
    else:
        print ("Error in PUD declaration, expected either: 'NONE', 'UP', or 'DOWN'")
        return

def setHigh(pin):
    GPIO.output(pin, GPIO.HIGH)

def setLow(pin):
    GPIO.output(pin, GPIO.LOW)

def read(pin):
    return GPIO.input(pin)

def closeGPIO():
    GPIO.cleanup()
