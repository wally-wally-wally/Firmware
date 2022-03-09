from serial import Serial

UART_0 = '/dev/ttyS0'
UART_1 = '/dev/ttyAMA0'

class UART():
    def __init__(self, port, baud):
        self.serial = Serial(port, baud)

    def read(self, numBytes):
        return self.serial.read(numBytes)

    def write(self, data):
        self.serial.write(data)

    def flush(self):
        self.serial.flushInput()

    def __del__(self):
        self.serial.close()
