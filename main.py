import threading
from system_monitor import sysMon
from main_task import mainTask

# Shared resources 
# Since we're accessing different pins I don't think locks are needed on GPIO functions 
#import GPIO

#lock = threading.Lock()

# General inits used by both threads
def init():
 #   GPIO.init()
    pass

if __name__ == '__main__':
  #  init()
    sysMon = threading.Thread(target=sysMon)
    mainTask = threading.Thread(target=mainTask)
       
    sysMon.start()
    mainTask.start()

    sysMon.join()
    mainTask.join()
