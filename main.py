import threading
from system_monitor import sysMon

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
    #main = threading.Thread(target=test2, args=(2,))
       
    sysMon.start()
    #main.start()

    sysMon.join()
    #main.join()
