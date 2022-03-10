#If not previously paired with an Android device it must be using bluetooth packages
#sudo bluetoothctl
#power on
#discoverable on
#pairable on
#pair <MAC_ADDRESS> - pi must respond yes

import bluetooth

class Socket:
    def __init__(self):
        self.server = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        self.server.bind(("",port))

    def advertise(self):
        self.server.listen(1)

    def connect(self):
        self.client, address = self.server.accept()
        print ("Accepted connection from", address)

    def read(self):
        return self.client.recv(1024).decode() #returns data read

    def write(self, data):
        self.client.send(data)

    def disconnect(self):
        self.client.close()
        self.server.close()

