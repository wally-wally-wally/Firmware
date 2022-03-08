from enum import IntEnum

class Commands(IntEnum):
    #Drive controls
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3
    CCW = 4
    CW = 5
    STOP = 6

    #Arm controls
    #ADD_CHECKPOINT
    #ARM_UP
    #ARM_DOWN
    #ARM_LEFT
    #ARM_RIGHT
    #ARM_FORWARD
    #ARM_BACKWARD
    #SET_CHEKPOINT

    #Task Controls
    START_RECORDING = 15
    END_RECORDING = 16
    RUN_TASK = 17
    LIST_TASKS = 18
