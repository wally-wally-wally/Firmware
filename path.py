#commented out sections haven't been tested - need aruco marker

import BLE
import BLDC
#import aruco
import time
from commands import Commands
from datetime import datetime

class FileManagement:
    def __init__(self, fileName):
        self.fileName = fileName
        self.createFile()

    def createFile(self):
        self.file = open(str(self.fileName) + ".txt", "w")

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
        self.file = open(str(self.fileName) + ".txt", "r")

    def openAppend(self):
        self.file = open(str(self.fileName) + ".txt", "a")

class PathManagement:
    def __init__(self, bleObject, navigationObject):
        self.BLE = bleObject
        self.navigate = navigationObject
        self.aruco_id = 0
        self.numLines = 0

    def executePath(self, pathName):
        with open(str(pathName) + ".txt") as f:
            for index, line in enumerate(f):
                self.executeSegment(line.strip())

    def executeSegment(self, line):			#if adding checkpoint with arm movement, can pass segment[1] in executeDirection
        segment = line.split()				#segment[1] would only be used in direction == checkpoint
        self.executeDirection(segment[0])
        time.sleep(int(float(segment[1])))
        self.navigate.stop()

    def executeDirection(self, direction):
        if direction == "forward":
            self.navigate.forward()
        elif direction == "backward":
            self.navigate.backward()
        elif direction == "right":
            self.navigate.right()
        elif direction == "left":
            self.navigate.left()
        elif direction == "CW":
            self.navigate.cw()
        elif direction == "CCW":
            self.navigate.ccw()
#        elif direction == "checkpoint":
#            do arm movement at designated aruco_id

    def recordPath(self, pathName):
        self.pathFile = FileManagement(pathName)
        self.pathFile.writeLine("start", "0")           #to set checkpoint it would be "set checkpoint command" sent by app - TBD
        data = self.BLE.read()

        while data != f'{Commands.END_TASK.value}'.encode():
            self.recordSegment(data)
            data = self.BLE.read()
#            if data == b'c\r\n':
#                self.setCheckpoint()

        self.atHomeBase()

    def recordSegment(self, data):
        direction = self.getDirection(data)
        travelTime = self.getTime()
        self.pathFile.writeLine(direction, travelTime)
        self.numLines += 1

    def atHomeBase(self):
#        rvec, tvec = aruco.estimatePose()
#        if not rvec and not tvec:
#            print("No aruco marker found. Reversing path back to home base.")
        self.reversePath()
        self.pathFile.writeFile("end", "0")        #no aruco_id because path was reversed
#        else:
#            self.pathFile.writeFile("end", self.aruco_id)

#    def setCheckpoint(self):
#        rvec, tvec = aruco.estimatePose()
#        if not rvec and not tvec:
#            print("Error: no aruco marker found. Can't set checkpoint here")
#        else:
#            self.pathFile.writeLine("checkpoint", self.aruco_id)
#            self.aruco_id += 1

    def getTime(self):                                  #times seem a bit off - check
        startTime = datetime.now()

        isStop = self.BLE.read()

        assert isStop == f'{Commonds.STOP.value}'.encode()

        endTime = datetime.now()
        timeString = endTime - startTime
        return timeString.total_seconds()

    def getDirection(self, direction):
        if direction == f'{Commands.FORWARD.value}'.encode():
            return "forward"
        elif direction == f'{Commands.BACKWARD.value}'.encode():
            return "backward"
        elif direction == f'{Commands.LEFT.value}'.encode():
            return "left"
        elif direction == f'{Commands.RIGHT.value}'.encode():
            return "right"
        elif direction == f'{Commands.CCW.value}'.encode()':
            return "CCW"
        elif direction == f'{Commands.CW.value}'.encode():
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
        return direction, segment[1]

    def reverseDirection(self, direction):
        if direction == "forward":
            return "backward"
        elif direction == "backward":
            return "forward"
        elif direction == "right":
            return "left"
        elif direction == "left":
            return "right"
        elif direction == "CW":
            return "CCW"
        elif direction == "CCW":
            return "CW"
