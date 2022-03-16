import PWM
import time

GRIPPER_PIN = 11
GRIPPER_FREQ = 400 # Hz

DUTY_CYCLE_CLOSED = 80 # %
DUTY_CYCLE_OPEN = 20 # %

MOVEMENT_TIME = 1 # s

class Gripper():
    def __init__(self):
        self.PWM = PWM.Signal(GRIPPER_PIN, GRIPPER_FREQ)

    def open(self):
        self.PWM.begin(DUTY_CYLCE_OPEN)
        # Stop PWM to stop parkinsons
        time.sleep(MOVEMENT_TIME)
        self.PWM.begin(0)
    
    def close(self):
        self.PWM.begin(DUTY_CYLCE_CLOSE)
        # Stop PWM to stop parkinsons
        time.sleep(MOVEMENT_TIME)
        self.PWM.begin(0)

