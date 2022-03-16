import gripper
import stepper
import time
import sys
sys.path.insert(1, 'matlab')
from IK import IK

STEPPER_DIR_PIN = [24, 8, 5]
STEPPER_ENABLE_PIN = 13
STEPPER_STEP_PIN = [25, 7, 6]
STEPPER_SPEED = 120

NUM_STEPPERS = 3

class Arm():
    def __init__(self):
        self.currentAngle = [0] * NUM_STEPPERS
        self.stepper = [0] * NUM_STEPPERS
        self.gripper = gripper.Gripper()
        for i in range(NUM_STEPPERS):
            self.stepper[i] = stepper.Stepper(STEPPER_STEP_PIN[i], STEPPER_DIR_PIN[i], STEPPER_ENABLE_PIN, STEPPER_SPEED)

    def enable(self):
        self.stepper[0].enableStepper()

    def disable(self):
        self.stepper[0].disableStepper()

    # x, y: x and y coordinates to move the arm relative to the base of the arm in metres. 
    def move(self, x, y):
        angles = IK([x,y,0])
        for i in range(NUM_STEPPERS):
            rotationDirection = 'CW'
            rotationAngle = angles[i] - self.currentAngle[i]
            if rotationAngle < 0:
                rotationDirection = 'CCW'
                rotationAngle = rotationAngle * -1
            self.stepper[i].setDirection(rotationDirection)
            self.stepper[i].rotate(rotationAngle)
        
