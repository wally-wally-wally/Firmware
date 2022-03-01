import GPIO
import PWM
import time

class Stepper:
    MICROSTEPS = 4      #from motor driver hardware setting
    ROTATION = 360      #degrees
    SECONDS = 60        #seconds per minute
    STEPANGLE = 1.8     #from stepper motor datasheet
    DUTYCYLCE = 50      #in percent
    RISINGEDGES = 16    #number of rising edges per full 360 rotation

    def __init__(self, stepPin, directionPin, enablePin, speed): #speed in rotations per minute
        GPIO.init()
        self.stepPin = stepPin
        self.directionPin = directionPin
        self.enablePin = enablePin

        GPIO.setPin(self.directionPin, 'OUT', 'NONE')
        GPIO.setPin(self.enablePin, 'OUT', 'NONE')

        self.setFrequency(speed)

    def setFrequency(self, speed):
        frequency = (speed*self.ROTATION*self.MICROSTEPS)/(self.SECONDS*self.STEPANGLE)

        if frequency > 250000:
            raise ValueError("Stepper speed is too high, frequency must be less than 250 000")
        else:
            self.pwmCtrl = PWM.Signal(self.stepPin, frequency)

    def setDirection(self, direction):
        if direction == 'CW':
            GPIO.write(self.directionPin, 'HIGH')
        elif direction == 'CCW':
            GPIO.write(self.directionPin, 'LOW')
        else:
            raise ValueError("Could not set stepper motor direction, expected either: 'CW' or 'CCW'")

    def rotate(self, degrees):        #degrees of rotation - home state is 45
        if degrees < 0:
            raise ValueError("Degrees is too low, please set it to a value between 0 and 360")
        elif degrees > 360:
            raise ValueError("Degrees is too high, please set it to a value between 0 and 360")
        else:
            delay = (RISINGEDGES*(1/self.frequency))*(degrees/self.ROTATION)
            startStepper()
            time.sleep(delay)
            stopStepper()

    def startStepper(self):
        self.pwmCtrl.begin(self.DUTYCYCLE)
    
    def stopStepper(self):
        self.pwmCtrl.stop()

    def enable(self):
        GPIO.write(self.enablePin, 'HIGH')

    def disable(self):
        GPIO.write(self.enablePin, 'LOW')