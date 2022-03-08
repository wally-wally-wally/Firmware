import GPIO
import PWM
import time

class Motor:
    DELAY = 0.2

    def __init__(self, pwmPin, directionPin, frequency):
        GPIO.init()
        self.pwmPin = pwmPin
        self.directionPin = directionPin
        self.speed = 0

        GPIO.setPin(self.directionPin, 'OUT', 'NONE')

        if frequency < 15000:
            raise ValueError("Frequency is too low, please set it to a value between 15000 and 25000")
        elif frequency > 25000:
            raise ValueError("Frequency is too high, please set it to a value between 15000 and 25000")
        else:
            self.pwmCtrl = PWM.Signal(pwmPin, frequency)

    def setDirection(self, direction):
        self.stop()
        if direction == 'CW':
            GPIO.write(self.directionPin, 'LOW')
        elif direction == 'CCW':
            GPIO.write(self.directionPin, 'HIGH')
        else:
            raise ValueError("Could not set motor direction, expected either: 'CW' or 'CCW'")
        time.sleep(self.DELAY)

    def setMotorSpeed(self, speed): #speed in percentage
        self.speed = speed

    def startMotor(self):
        self.pwmCtrl.begin(self.speed)

    def stopMotor(self):
        self.pwmCtrl.stop()
        time.sleep(self.DELAY)

class Navigation:
    def __init__(self, pwmPinFR, pwmPinFL, pwmPinBR, pwmPinBL, dirPinFR, dirPinFL, dirPinBR, dirPinBL, frequency):
        self.FR = Motor(pwmPinFR, dirPinFR, frequency)
        self.FL = Motor(pwmPinFL, dirPinFL, frequency)
        self.BR = Motor(pwmPinBR, dirPinBR, frequency)
        self.BL = Motor(pwmPinBL, dirPinBL, frequency)

    def forward(self):
        self.stop()
        self.FR.setDirection('CCW') #forward
        self.FL.setDirection('CW')  #forward
        self.BR.setDirection('CCW') #forward
        self.BL.setDirection('CW')  #forward
        self.start()

    def backward(self):
        self.stop()
        self.FR.setDirection('CW')  #backward
        self.FL.setDirection('CCW') #backward
        self.BR.setDirection('CW')  #backward
        self.BL.setDirection('CCW') #backward
        self.start()

    def right(self):
        self.stop()
        self.FR.setDirection('CW')  #backward
        self.FL.setDirection('CW')  #forward
        self.BR.setDirection('CCW') #forward
        self.BL.setDirection('CCW') #backward
        self.start()

    def left(self):
        self.stop()
        self.FR.setDirection('CCW') #forward
        self.FL.setDirection('CCW') #backward
        self.BR.setDirection('CW')  #backward
        self.BL.setDirection('CW')  #forward
        self.start()

    def ccw(self):
        self.stop()
        self.FR.setDirection('CCW') #forward
        self.FL.setDirection('CCW') #backward
        self.BR.setDirection('CCW') #forward
        self.BL.setDirection('CCW') #backward
        self.start()

    def cw(self):
        self.stop()
        self.FR.setDirection('CW') #backward
        self.FL.setDirection('CW') #forward
        self.BR.setDirection('CW') #backward
        self.BL.setDirection('CW') #forward
        self.start()
    
    def setSpeed(self, speed):      #add buffers if necessary
        self.FR.setMotorSpeed(int(speed))
        self.FL.setMotorSpeed(int(speed))
        self.BR.setMotorSpeed(int(speed))
        self.BL.setMotorSpeed(int(speed))
    
    def stop(self):
        self.FR.stopMotor()
        self.FL.stopMotor()
        self.BR.stopMotor()
        self.BL.stopMotor()
    
    def start(self):
        self.FR.startMotor()
        self.FL.startMotor()
        self.BR.startMotor()
        self.BL.startMotor()
