#If not previously paired with an Android device it must be using bluetooth packages
#sudo bluetoothctl
#power on
#discoverable on
#pairable on
#pair <MAC_ADDRESS> - pi must respond yes

import bluetooth

def init():
    server = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server.bind(("",port))
    return server            #must be stored and passed

def advertise(server):
    server.listen(1)

def connect(server):
    client,address = server.accept()
    print ("Accepted connection from ",address)
    return client            #must be stored and passed

def read(client):
    return client.recv(1024) #returns data read

def write(client, data):
    client.send(data)

def disconnect(client, server):
    client.close()
    server.close()

