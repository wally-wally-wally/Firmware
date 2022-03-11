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
    def __init__(self, bleObject, navigationObject, cameraObject):
        self.ble = bleObject
        self.navigate = navigationObject
        self.camera = cameraObject
        self.numLines = 0

    def executePath(self, pathName):
        with open(TASKS_FOLDER + str(pathName)) as f:
            for index, line in enumerate(f):
                self.executeSegment(line.strip())

    def executeSegment(self, line):			#if adding checkpoint with arm movement, can pass segment[1] in executeDirection
        segment = line.split()				#segment[1] would only be used in direction == checkpoint
        self.executeDirection(segment[0])

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
        time.sleep(0.5)

    def executeDirection(self, direction):
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
#        elif direction == "checkpoint":
#            do arm movement at designated aruco id

    def recordPath(self, pathName):
        self.pathFile = FileManagement(pathName)
        self.pathFile.writeLine("start", "0")           #to set checkpoint it would be "set checkpoint command" sent by app - TBD
        data = self.ble.read()

        while data != f'{Commands.END_RECORDING.value}':
            self.recordSegment(data)
            data = self.ble.read()
#            if data == b'c\r\n':
#                self.setCheckpoint()

        self.atHomeBase()

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
            self.pathFile.writeLine("end", "0")        #no aruco id because path was reversed
        else:
            self.pathFile.openAppend()
            self.pathFile.writeLine("end", "0")

#    def setCheckpoint(self):
#        rvec, tvec = aruco.estimatePose()
#        if not rvec and not tvec:
#            print("Error: no aruco marker found. Can't set checkpoint here")
#        else:
#            self.pathFile.writeLine("checkpoint", getArucoID())

    def getTime(self):                                  #times seem a bit off - check
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
            return "forward"
        elif direction == f'{Commands.BACKWARD.value}':
            self.navigate.backward()
            return "backward"
        elif direction == f'{Commands.LEFT.value}':
            self.navigate.left()
            return "left"
        elif direction == f'{Commands.RIGHT.value}':
            self.navigate.right()
            return "right"
        elif direction == f'{Commands.CCW.value}':
            self.navigate.ccw()
            return "CCW"
        elif direction == f'{Commands.CW.value}':
            self.navigate.cw()
            return "CW"

    def reversePath(self):
        while self.numLines != 0:
            direction, time = self.reverseSegment()
            self.pathFile.openAppend()
            self.pathFile.writeLine(direction, time)

    def reverseSegment(self):
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
            return "backward"
        elif direction == "backward":
            self.navigate.forward()
            return "forward"
        elif direction == "right":
            self.navigate.left()
            return "left"
        elif direction == "left":
            self.navigate.right()
            return "right"
        elif direction == "CW":
            self.navigate.ccw()
            return "CCW"
        elif direction == "CCW":
            self.navigate.cw()
            return "CW"

    def listTasks(self):
        tasks = os.listdir("/home/pi/code/firmware/tasks")
        arr = ','.join(tasks)
        self.ble.write(f"{arr}\n")
