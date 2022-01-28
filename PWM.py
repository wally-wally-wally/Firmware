import RPi.GPIO as RPi_IO
import GPIO

class Signal:
    def __init__(self, pin, frequency):
        GPIO.init()
        GPIO.setPin(pin, 'OUT', 'NONE')
        self.pwm = RPi_IO.PWM(pin, frequency)

    def begin(self, dutyCycle):             #dutyCycle is in % (write 50 for 50%)
        self.pwm.start(dutyCycle)

    def setDutyCycle(self, dutyCycle):
        self.pwm.ChangeDutyCycle(dutyCycle)

    def stop(self):
        self.pwm.stop()
