import uart
import math

DATA_HEADER_LOWER = 'aa'
DATA_HEADER_UPPER = '55'

BAUD = 115200
PORT = uart.UART_0

class Lidar():
    def __init__(self, uart):
        self.uart = uart

    def readData(self):
        self.uart.flush()
        headerReceived = False
        while(headerReceived is False):
            while (self.uart.read(1).hex() != DATA_HEADER_LOWER):
                pass
            if (self.uart.read(1).hex() == DATA_HEADER_UPPER):
                if(self.uart.read(1).hex() != '01'):
                    headerReceived = True

        self.numVals = int(self.uart.read(1).hex(), 16)

        tmpL = self.uart.read(1)
        fsaL = tmpL[0]
        
        tmpU = self.uart.read(1)
        fsaU = tmpU[0]
        
        self.fsa = (fsaU * 256) + fsaL
        
        tmpL = self.uart.read(1)
        lsaL = tmpL[0]

        tmpU = self.uart.read(1)
        lsaU = tmpU[0]

        self.lsa = (lsaU * 256) + lsaL

        csL = self.uart.read(1).hex()
        csU = self.uart.read(1).hex()
        self.cs = int(csU + csL, 16)

        self.rawData = self.uart.read(self.numVals * 2)
        self.dist = [0] * self.numVals
        self.ang =  [0] * self.numVals

    def dataCorrection(self):
        checksum = 0x55AA
        checksum ^= self.fsa

        startAng = (self.fsa >> 1) / 64
        endAng   = (self.lsa >> 1) / 64

        diff = endAng - startAng
        if diff < 0:
            diff += 360

        for i in range(self.numVals):
            distL = self.rawData[i * 2]
            distU = self.rawData[i * 2 + 1]

            self.dist[i] = distU * 256 + distL

            checksum ^= self.dist[i]

            self.dist[i] = self.distCorrection(self.dist[i])
            ang = self.angCorrection1(diff, startAng, i)
            self.ang[i] = self.angCorrection2(self.dist[i], ang)
            if self.ang[i] < 0:
                self.ang[i] = self.ang[i] + 360
            elif self.ang[i] >= 360:
                self.ang[i] = self.ang[i] - 360

            # Error
            if self.dist[i] == 0 or self.dist[i] == 0.5:
                self.dist[i] = 0.0
                self.ang[i] = 0.0

        checksum ^= (self.numVals << 8)
        checksum ^= (self.lsa)
        return checksum == self.cs

    def distCorrection(self, s):
        return s / 4

    # i: index, starting from 0
    def angCorrection1(self, angDiff, startAng, i):
        if self.numVals == 1:
            return startAng
        return (angDiff / (self.numVals - 1)) * (i) + startAng

    # dist: the corrected distance, ang: the corrected angle from angCorrection1
    def angCorrection2(self, dist, ang):
        if (dist == 0):
            angCorrection = 0
        else:
            angCorrection = math.degrees(math.atan(21.8 * ((155.3 - dist) / (155.3 * dist)) ))
        return ang + angCorrection
