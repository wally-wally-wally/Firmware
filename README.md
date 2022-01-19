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


**ArUco**

The camera must be calibrated before (proper) use. Currently, the camera is NOT calibrated.
The file `cal_chessboard.png` needs to be printed out and several pictures need to be taken with the Pi camera in different orientations.
Then calibration.py needs to be run to generate two numpy files `calibration_matrix.npy` and `distortion_coefficients.npy` (the current ones are for a
different camera)

`python calibration.py --dir calibration_checkerboard/ --square_size 0.024`
