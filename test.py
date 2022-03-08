import uart
import lidar
import time

u = uart.UART('COM5', 115200)
l = lidar.Lidar(u)

time.sleep(5)
print('Beginning', flush = True)
obstruction = False
data = [False] * 360
while True:
    l.readData()
    l.dataCorrection()


    for i in range(len(l.dist)):
        if l.ang[i] > 0 or l.ang[i] < 360:
            if l.dist[i] < 200:
                data[round(l.ang[i])] = True
                if obstruction is False:
                    print('New obstruction', flush = True)
                obstruction = True
            else:
                data[round(l.ang[i])] = False

    old = obstruction
    obstruction = False
    for i in range(85, 135):
        if data[i] is True:
            obstruction = True
            break
    if obstruction is False and old is True:
        print ('Obstruction Removed', flush = True)        
        #print(str(l.ang[i]) + ": " + str(l.dist[i]))
    #time.sleep(1)

