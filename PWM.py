#code works along side GPIO.py
#the init in GPIO.py must be called before any of these functions are called

import RPi.GPIO as GPIO

def setPin(pin, frequency):
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.PWM(pin, frequency)    #this value is pwm in subsequent function calls

def begin(pwm, dutyCycle):             #dutyCycle is in % (write 50 for 50%)
    pwm.start(dutyCycle)

def setDutyCycle(pwm, dutyCycle):
    pwm.ChangeDutyCycle(dutyCycle)

def stop(pwm):
    pwm.stop()
