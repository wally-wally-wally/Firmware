import uart
import math

DATA_HEADER_LOWER = 'aa'
DATA_HEADER_UPPER = '5500'

BAUD = 115200
UART = uart.UART_0

class Lidar():
    def __init__(self, uart):
        self.uart = uart

    def readData(self):
        self.uart.flush()
        headerReceived = False
        while(headerReceived is False):
            while (self.uart.read(1).hex() != DATA_HEADER_LOWER):
                pass
            if (self.uart.read(2).hex() == DATA_HEADER_UPPER):
                headerReceived = True

        self.numVals = int(self.uart.read(1).hex(), 16)

        fsaL = self.uart.read(1).hex()
        fsaU = self.uart.read(1).hex()
        self.fsa = int(fsaU + fsaL, 16)
        
        lsaL = self.uart.read(1).hex()
        lsaU = self.uart.read(1).hex()
        self.lsa = int(lsaU + lsaL, 16)

        csL = self.uart.read(1).hex()
        csU = self.uart.read(1).hex()
        self.cs = int(csU + csL, 16)

        self.rawData = self.uart.read(self.numVals * 2).hex()
        self.dist = [0] * self.numVals
        self.ang =  [0] * self.numVals

    def dataCorrection(self):
        checksum = 0x55AA
        checksum ^= self.fsa

        startAng = (self.fsa >> 1) / 64
        endAng   = (self.lsa >> 1) / 64

        diff = endAng - startAng
        #if diff < 0:
        #    diff += 360

        for i in range(self.numVals):
            distL = self.rawData[i * 4] + self.rawData[i * 4 + 1]
            distU = self.rawData[(i * 4 ) + 2] + self.rawData[(i * 4 ) + 3]
            self.dist[i] = int(distU + distL, 16)

            checksum ^= self.dist[i]

            self.dist[i] = self.distCorrection(self.dist[i])
            ang = self.angCorrection1(diff, startAng, i)
            self.ang[i] = self.angCorrection2(self.dist[i], ang)

        checksum ^= (self.numVals << 8)
        checksum ^= (self.lsa)
        return checksum == self.cs

    def distCorrection(self, s):
        return s / 4

    # i: index, starting from 0
    def angCorrection1(self, angDiff, startAng, i):
        return (angDiff / (self.numVals - 1)) * (i) + startAng

    # dist: the corrected distance, ang: the corrected angle from angCorrection1
    def angCorrection2(self, dist, ang):
        if (dist == 0):

