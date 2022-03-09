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
        #print(str(l.ang[i]) + ": " + str(l.dist[i]))
        if l.ang[i] == 0:
            continue
        rounded = round(l.ang[i])
        if rounded >= 360:
            rounded = rounded - 360
        if l.ang[i] > 240 or l.ang[i] < 290:
            if l.dist[i] < 200 and l.dist[i] != 0:
                #if(data[rounded] is True):
                if obstruction is False:
                    print('New obstruction', flush = True)
                obstruction = True
                data[rounded] = True

            else:
                data[rounded] = False

    old = obstruction
    obstruction = False
    for i in range(240, 290):
        if data[i] is True:
            obstruction = True
            break
    if obstruction is False and old is True:
        print ('Obstruction Removed', flush = True)        
        #print(str(l.ang[i]) + ": " + str(l.dist[i]))
    #time.sleep(1)

