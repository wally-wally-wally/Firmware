# Firmware

**Bluetooth**

The following packages must be installed:

```sudo apt-get install bluetooth libbluetooth-dev bluez```

```sudo pip3 install pybluez```(might not be necessary)


The bluez.service file also needs to be updated:

```sudo nano /etc/systemd/system/dbus-org.bluez.service```

In the third line in the [Service] section, we need to add -C to the end 
of the line: ```ExecStart=/usr/lib/bluetooth/bluetoothd -C```

And right below that line, we need to add the following new line:```ExecStartPost=/usr/bin/sdptool add SP```