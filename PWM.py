#code works along side GPIO.py
#the init in GPIO.py must be called before any of these functions are called

import RPi.GPIO as GPIO

class signal:
    def setPin(signal, pin, frequency):
        GPIO.setup(pin, GPIO.OUT)
        signal.pwm = GPIO.PWM(pin, frequency)

    def begin(signal, dutyCycle):             #dutyCycle is in % (write 50 for 50%)
        signal.pwm.start(dutyCycle)

    def setDutyCycle(signal, dutyCycle):
        signal.pwm.ChangeDutyCycle(dutyCycle)

    def stop(signal):
        signal.pwm.stop()
