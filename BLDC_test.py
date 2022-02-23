import BLDC

pwmFR =
pwmFL =
pwmBR =
pwmBL =
dirFR =
dirFL =
dirBR =
dirBL =
frequency =

wally = Navigation(pwmFR, pwmFL, pwmBR, pwmBL, dirFR, dirFL, dirBR, dirBL, frequency)

wally.setSpeed(0)

while(1):
    print ("Enter input:")
    data = input()
    if data == 'forward':
        wally.forward()
    elif data == 'backward':
        wally.backward()
    elif data == 'right':
        wally.right()
    elif data == 'left':
        wally.left()
    elif data == 'ccw':
        wally.ccw()
    elif data == 'cw':
        wally.cw()
    elif data == 'speed':
        print ("Enter speed:")
        speed = input()
        wally.setSpeed(int(speed))
    elif data == 'stop':
        wally.stop()
    elif data == 'start':
        wally.start()
    elif data == 'quit':
        break