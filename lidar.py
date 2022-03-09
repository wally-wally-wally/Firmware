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
            if (self.uart.read(1).hex() == '55'):
                if(self.uart.read(1).hex() != '01'):
                    headerReceived = True

        self.numVals = int(self.uart.read(1).hex(), 16)

        #fsaL = self.uart.read(1).hex()
        tmpL = self.uart.read(1)
        fsaL = tmpL[0]
        #print(tmpL)
        #print(fsaL)
        #print(tmpL[0])
        #fsaL = tmpL.hex()
        #print(int(fsaL, 16))
        tmpU = self.uart.read(1)
        fsaU = tmpU[0]
        #print(tmpU)
        #print(fsaU)
        
        #print(int(fsaU, 16))
        #self.fsa = int(fsaU + fsaL, 16)
        self.fsa = (fsaU * 256) + fsaL
        #print(str(self.fsa) + '\n')
        #print('fsa: ' + str(self.fsa))
        #print('fsaNew: ' + str(tmpL + tmpU *256))
        
        #lsaL = self.uart.read(1).hex()
        #lsaU = self.uart.read(1).hex()
        tmpL = self.uart.read(1)
        lsaL = tmpL[0]
        tmpU = self.uart.read(1)
        lsaU = tmpU[0]
        self.lsa = (lsaU * 256) + lsaL

        #self.lsa = int(lsaU + lsaL, 16)

        csL = self.uart.read(1).hex()
        csU = self.uart.read(1).hex()
        self.cs = int(csU + csL, 16)

        self.rawData = self.uart.read(self.numVals * 2)#.hex()
        self.dist = [0] * self.numVals
        self.ang =  [0] * self.numVals

    def dataCorrection(self):
        checksum = 0x55AA
        checksum ^= self.fsa

        startAng = (self.fsa >> 1) / 64
        endAng   = (self.lsa >> 1) / 64
        #print('start: ' + str(startAng))
        #print('end: ' + str(endAng))


        diff = endAng - startAng
        if diff < 0:
            diff += 360

        for i in range(self.numVals):
            #distL = self.rawData[i * 4] + 256 * self.rawData[i * 4 + 1]
            distL = self.rawData[i * 2]
            distU = self.rawData[i * 2 + 1]
            #distU = self.rawData[(i * 4 ) + 2] + 256 * self.rawData[(i * 4 ) + 3]
            #self.dist[i] = int(distU + distL, 16)
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

