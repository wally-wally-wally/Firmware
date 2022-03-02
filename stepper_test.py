import stepper

stepPin = 
directionPin = 
enablePin = 
speed = 

motor = stepper.Stepper(stepPin, directionPin, enablePin, speed)
motor.enable()

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
    elif data == 'enable':
        print("Enabling steppers")
        motor.enable()
    elif data == 'disable':
        print("Disabling steppers")
        motor.disable()
    elif data == 'quit':
        break
