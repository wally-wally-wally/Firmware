#If not previously paired with an Android device it must be using bluetooth packages
#sudo bluetoothctl
#power on
#discoverable on
#pairable on
#pair <MAC_ADDRESS> - pi must respond yes

import bluetooth

class Socket:
    def __init__(socket):
        socket.server = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        socket.server.bind(("",port))

    def advertise(socket):
        socket.server.listen(1)

    def connect(socket):
        socket.client, address = socket.server.accept()
        print ("Accepted connection from", address)

    def read(socket):
        return socket.client.recv(1024) #returns data read

    def write(socket, data):
        socket.client.send(data)

    def disconnect(socket):
        socket.client.close()
        socket.server.close()

