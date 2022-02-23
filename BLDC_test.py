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

wally.setSpeed(20)
tracker = 0

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
    elif data == 's':
        tracker = tracker^1
        if tracker == 1:
            wally.start()
        elif tracker == 0:
            wally.stop()
    elif data == 'quit':
        break