import time
import BLE
import BLDC

class FileManagement:
    def __init__(self, fileName):
        self.fileName = fileName
        self.createFile()
    
    def createFile(self):
        self.file = open(str(self.fileName) + ".txt", "a")

    def writeLine(self, direction, time):
        self.file.write(str(direction) + " " + str(time) + "\n")

    def readLine(self, desiredLine):
        self.openFile()
        self.file.seek(0)
        lines = self.file.readlines()

        for index, line in enumerate(lines):
            if index == desiredLine:
                return line.strip()

    def closeFile(self):
        self.file.close()

    def openFile(self):
        self.file = open(str(self.fileName) + ".txt", "r")

class Path:
    def __init__(self, pathName, bleObject):
        self.pathFile = FileManagement(pathName)
        self.BLE = bleObject

    def readBLE(self):
        data = self.BLE.read()
        print(str(data))
    
    #def executePath(self):
    #    lines = self.pathFile.readFile()
    #    for segment in enumerate(lines):
    #        executeSegment(segment.strip())

    #def executeSegment(self, command):
        #read direction and distance at line and execute

    #def recordPath(self):
     #   self.pathFile.writeLine("start", "0")
    #    while not atHomeBase():
    
    def recordSegment(self):
        direction = getDirection()
        travelTime = getTime()
        self.pathFile.writeLine(direction, travelTime)

    #def atHomeBase(self, aruco_id):
    #    check for aruco marker, if not there:
      #      reversePath()
     #   if there is aruco
      #      self.pathFile.writeFile("end", 0)

    #def setCheckpoint(self, aruco_id):
        #check for aruco marker, if not there throw error, else:
        #get aruco id
     #   self.pathFile.write("checkpoint", aruco_id)

    def getTime(self):
        startTime = time.localtime()

        startDirection = self.BLE.read()
        endDirection = startDirection

        while (startDirection == endDirection):
            endDirection = self.BLE.read()

        endTime = time.localtime()
        return (endTime - startTime)
    
    def getDirection(self):      #numbers should be changed based on BLE inputs
        direction = self.BLE.read()
        if direction == 0:
            return 'forward'
        elif direction == 1:
            return 'backward'
        elif direction == 2:
            return 'right'
        elif direction == 3:
            return 'left'
        elif direction == 4:
            return 'CW'
        elif direction == 5:
            return 'CCW'

    #def reversePath(self):          #this is reading the file in order, probably want to read backwards?
    #    lines = self.pathFile.readFile()
    #    for segment in enumerate(lines):
    #        reverseSegment(segment.strip())

    #def reverseSegment(self:)
        #read file line by line from the bottom up
        #write at the bottom the reverse
