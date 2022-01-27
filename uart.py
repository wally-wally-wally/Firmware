import serial

UART_0 = '/dev/ttyS0'
UART_1 = '/dev/ttyAMA0'

class UART():
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)

    def read(self):
        return self.ser.read()

    def write(self, data):
        self.ser.write(data)

    def __del__(self):
        self.ser.close()

