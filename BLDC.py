import GPIO
import PWM
import time

class Motor:
    def __init__(self, pwmPin, directionPin, frequency):
        GPIO.init()
        self.pwmPin = pwmPin
        self.directionPin = directionPin
        self.speed = 0
        self.delay = 0.2
        GPIO.setPin(self.directionPin, 'OUT', 'NONE')

        if frequency < 15000:
            raise ValueError("Frequency is too low, please set it to a value between 15000 and 25000")
        elif frequency > 25000:
            raise ValueError("Frequency is too high, please set it to a value between 15000 and 25000")
        else:
            self.pwmCtrl = PWM.Signal(pwmPin, frequency)

    def setDirection(self, direction):
        self.stop()
        time.sleep(self.delay)
        if direction == 'CW':
            GPIO.write(self.directionPin, 'LOW')
        elif direction == 'CCW':
            GPIO.write(self.directionPin, 'HIGH')
        else:
            raise ValueError("Could not set motor direction, expected either: 'CW' or 'CCW'")
        time.sleep(self.delay)

    def setSpeed(self, speed):                     #speed in percentage
        self.stop()
        self.speed = speed
        time.sleep(self.delay)

    def start(self):
        self.pwmCtrl.begin(self.speed)

    def stop(self):
        self.speed = 0
        self.pwmCtrl.stop()
