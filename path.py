import BLE
import BLDC
import aruco
import time
import os
import camera
import global_vars
from commands import Commands
from datetime import datetime

TASKS_FOLDER = './tasks/'

class FileManagement:
    def __init__(self, fileName):
        self.fileName = fileName
        self.createFile()

    def createFile(self):
        self.file = open(TASKS_FOLDER + str(self.fileName), "w")

    def writeLine(self, direction, time):
        self.file.write(str(direction) + " " + str(time) + "\n")

    def readLine(self, desiredLine):
        self.openRead()
        self.file.seek(0)
        lines = self.file.readlines()

        for index, line in enumerate(lines):
            if index == desiredLine:
                return line.strip()

    def closeFile(self):
        self.file.close()

    def openRead(self):
        self.file = open(TASKS_FOLDER + str(self.fileName), "r")

    def openAppend(self):
        self.file = open(TASKS_FOLDER + str(self.fileName), "a")

class PathManagement:

    INCREMENT = 0.05

    def __init__(self, bleObject, navigationObject, cameraObject): #add arm object
        self.ble = bleObject
        self.navigate = navigationObject
        self.camera = cameraObject
        #self.arm = armObject
        self.armMoving = False
        self.numLines = 0

    def executePath(self, pathName):
        with open(TASKS_FOLDER + str(pathName)) as f:
            for index, line in enumerate(f):
                self.executeSegment(line.strip())

    def executeSegment(self, line):
        segment = line.split()
        self.executeDirection(segment[0], segment[1], segment[2])

        if not armMoving:
            endTime = time.time() + float(segment[1])
            while time.time() < endTime:
                if global_vars.CollisionDetected:
                    timeLeft = endTime - time.time()
                    self.navigate.stop()
                    while global_vars.CollisionDetected:
                        time.sleep(0.2)
                    self.executeDirection(segment[0])
                    endTime = time.time() + timeLeft

            self.navigate.stop()

        self.armMoving = False
        time.sleep(0.5)

    def executeDirection(self, direction, position1, position2):
        if direction == "forward":
            self.navigate.forward()
            global_vars.WallyDirection = 'F'
        elif direction == "backward":
            self.navigate.backward()
            global_vars.WallyDirection = 'B'
        elif direction == "right":
            self.navigate.right()
            global_vars.WallyDirection = 'R'
        elif direction == "left":
            self.navigate.left()
            global_vars.WallyDirection = 'L'
        elif direction == "CW":
            self.navigate.cw()
            global_vars.WallyDirection = 'N'
        elif direction == "CCW":
            self.navigate.ccw()
            global_vars.WallyDirection = 'N'
        elif direction == "gripper":
            if position1 == "1":
                #self.arm.openGrip()
                print("open grip")
            elif position1 == "0":
                #self.arm.closeGrip()
                print("close grip")
            self.armMoving = True
        elif direction == "arm":
            #self.arm.move(position1, position2)
            print("moving arm")
            self.armMoving = True

    def recordPath(self, pathName):
        self.pathFile = FileManagement(pathName)
        self.pathFile.writeLine("start", "0")

        self.setGripper()

        data = self.ble.read()

        while data != f'{Commands.END_RECORDING.value}':
            if data == f'{Commands.ADD_CHECKPOINT.value}':
                self.setCheckpoint()
            else:
                self.recordSegment(data)

            data = self.ble.read()

        self.atHomeBase()
        self.setGripper()
        self.pathFile.closeFile()

    def recordSegment(self, data):
        direction = self.getDirection(data)
        travelTime = self.getTime()
        self.pathFile.writeLine(direction, travelTime)
        self.numLines += 1

    def atHomeBase(self):
        time.sleep(0.5)
        self.camera.capture("home")
        if not aruco.getIds("home"):
            print("No aruco marker found. Reversing path back to home base.")
            self.reversePath()
            self.pathFile.writeLine("end", "0")
        else:
            self.numLines = 0
            self.pathFile.openAppend()
            self.pathFile.writeLine("end", "0")

    def setCheckpoint(self):
        time.sleep(0.5)
        self.camera.capture("checkpoint")
        if not aruco.getIds("checkpoint"):
            print("Error: no aruco marker found. Can't set checkpoint here")
            self.ble.write(f"0\n") #no aruco
        else:
            self.ble.write(f"1\n") #found aruco
            data = self.ble.read()

            while data != f'{Commands.SET_CHECKPOINT.value}':
                #position1, position2 = self.arm.getCurrentPosition()

                if data == f'{Commands.ARM_UP.value}':
                    #self.arm.move(position1, position2 + self.INCREMENT)
                    print("arm up")
                elif direction == f'{Commands.ARM_DOWN.value}':
                    #self.arm.move(position1, position2 - self.INCREMENT)
                    print("arm down")
                elif direction == f'{Commands.ARM_FORWARD.value}':
                    #self.arm.move(position1 + self.INCREMENT, position2)
                    print("arm forward")
                elif direction == f'{Commands.ARM_BACKWARD.value}':
                    #self.arm.move(position1 - self.INCREMENT, position2)
                    print("arm backward")
                elif direction == f'{Commands.TOGGLE_GRIPPER.value}':
                    self.writeArmPosition()

                    status = True #self.arm.isOpen()
                    if status == True:
                #        self.arm.closeGrip()
                        self.pathFile.writeLine("gripper", "0")
                        self.numLines += 1
                    elif status == False:
                #        self.arm.openGrip()
                        self.pathFile.writeLine("gripper", "1")
                        self.numLines += 1
            
            self.writeArmPosition()

    def setGripper(self):
        #status = self.arm.isOpen()
        #if status == False:
        #    self.arm.openGrip()
        print("setting grip")

    def writeArmPosition(self):
        #position1, position2 = self.arm.getCurrentPosition()
        self.pathFile.writeLine("arm", "position1", "position2")
        self.numLines += 1

    def getTime(self):
        startTime = datetime.now()

        isStop = self.ble.read()

        assert isStop == f'{Commands.STOP.value}'

        self.navigate.stop()

        endTime = datetime.now()
        timeString = endTime - startTime
        return timeString.total_seconds()

    def getDirection(self, direction):
        if direction == f'{Commands.FORWARD.value}':
            self.navigate.forward()
            print("forward")
            return "forward"
        elif direction == f'{Commands.BACKWARD.value}':
            self.navigate.backward()
            print("backward")
            return "backward"
        elif direction == f'{Commands.LEFT.value}':
            self.navigate.left()
            print("left")
            return "left"
        elif direction == f'{Commands.RIGHT.value}':
            self.navigate.right()
            print("right")
            return "right"
        elif direction == f'{Commands.CCW.value}':
            self.navigate.ccw()
            print("CCW")
            return "CCW"
        elif direction == f'{Commands.CW.value}':
            self.navigate.cw()
            print("CW")
            return "CW"

    def reversePath(self):
        while self.numLines != 0:
            direction, time = self.reverseSegment()
            self.pathFile.openAppend()
            self.pathFile.writeLine(direction, time)

    def reverseSegment(self):
        line = self.pathFile.readLine(self.numLines)
        segment = line.split()
        
        while segment[0] == "arm" or "gripper":
            self.numLines -= 1
            line = self.pathFile.readLine(self.numLines)
            segment = line.split()

        direction = self.reverseDirection(segment[0])
        self.numLines -= 1

        endTime = time.time() + float(segment[1])
        while time.time() < endTime:
            pass

        self.navigate.stop()
        time.sleep(0.5)

        return direction, segment[1]

    def reverseDirection(self, direction):
        if direction == "forward":
            self.navigate.backward()
            print("backward")
            return "backward"
        elif direction == "backward":
            self.navigate.forward()
            print("forward")
            return "forward"
        elif direction == "right":
            self.navigate.left()
            print("left")
            return "left"
        elif direction == "left":
            self.navigate.right()
            print("right")
            return "right"
        elif direction == "CW":
            self.navigate.ccw()
            print("CCW")
            return "CCW"
        elif direction == "CCW":
            self.navigate.cw()
            print("CW")
            return "CW"

    def listTasks(self):
        tasks = os.listdir("/home/pi/code/firmware/tasks")
        arr = ','.join(tasks)
        self.ble.write(f"{arr}\n")
