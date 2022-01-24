import GPIO
import PWM

class Motor:
    def __init__(self, pwmPin, directionPin):
        self.pwmCtrl = PWM.Signal()
        self.pwmPin = pwmPin
        self.directionPin = directionPin
        self.speed = 0
        GPIO.setPin(self.directionPin, 'OUT', 'NONE')

    def setFrequency(self, frequency):
        if frequency < 15000:
            raise ValueError("Frequency is too low, please set it to a value between 15000 and 25000")
        elif frequency > 25000:
            raise ValueError("Frequency is too high, please set it to a value between 15000 and 25000")
        else:
            self.pwmCtrl.setPin(self.pwmPin, frequency)

    def setDirection(self, direction):
        if direction == 'CW':
            GPIO.write(self.directionPin, 'LOW')
        elif direction == 'CCW':
            GPIO.write(self.directionPin, 'HIGH')
        else:
            raise ValueError("Could not set motor direction, expected either: 'CW' or 'CCW'")

    def setSpeed(self, speed):                     #speed in percentage
        if speed < 50:
            raise ValueError("Speed is too low, please set it to a value higher than 50%")
        else:
            self.speed = speed

    def start(self):
        self.pwmCtrl.begin(self.speed)

    def stop(self):
        self.pwmCtrl.stop()
