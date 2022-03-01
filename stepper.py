import GPIO
import PWM

class Stepper:
    def __init__(self, stepPin, directionPin, enablePin, frequency):
        GPIO.init()
        self.stepPin = stepPin
        self.directionPin = directionPin
        self.enablePin = enablePin
        self.step = 0

        GPIO.setPin(self.directionPin, 'OUT', 'NONE')
        GPIO.setPin(self.enablePin, 'OUT', 'NONE')

        if frequency > 250000:
            raise ValueError("Stepper frequency is too high, please set it to a value less than 250 000")
        else:
            self.pwmCtrl = PWM.Signal(stepPin, frequency)

    def setDirection(self, direction):
        #stop?
        if direction == 'CW':
            GPIO.write(self.directionPin, 'HIGH')
        elif direction == 'CCW':
            GPIO.write(self.directionPin, 'LOW')
        else:
            raise ValueError("Could not set stepper motor direction, expected either: 'CW' or 'CCW'")

    def setStep(self, step):        #step in percent - degree of movement
        #TO DO: change to take in degrees and convert it to duty cycle (using quarter step)
        self.step = step

    def startStepper(self):
        self.pwmCtrl.begin(self.step)
    
    def stopStepper(self):
        self.pwmCtrl.stop()

    def enable(self):
        GPIO.write(self.enablePin, 'HIGH')

    def disable(self):
        GPIO.write(self.enablePin, 'LOW')