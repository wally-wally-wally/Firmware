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
    ADD_CHECKPOINT = 7
    ARM_UP = 8
    ARM_DOWN = 9
    ARM_LEFT = 10
    ARM_RIGHT = 11
    ARM_FORWARD = 12
    ARM_BACKWARD = 13
    SET_CHECKPOINT = 14

    #Task Controls
    START_RECORDING = 15
    END_RECORDING = 16
    RUN_TASK = 17
    LIST_TASKS = 18

    TOGGLE_GRIPPER = 19
