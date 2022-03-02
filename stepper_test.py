import stepper

stepPin = 18
directionPin = 23
speed = 120

motor = stepper.Stepper(stepPin, directionPin, speed)

while (1):
    print("Enter input:")
    data = input()
    if data == 'direction':
        print("Enter direction:")
        dir = input()
        motor.setDirection(dir)
    elif data == 'rotate':
        print("Enter degrees of rotation:")
        deg = input()
        motor.rot(deg)
    elif data == 'start':
        print("Starting motor")
        motor.startStepper()
    elif data == 'stop':
        print("Stopping motor")
        motor.stopStepper()
    elif data == 'quit':
        break
