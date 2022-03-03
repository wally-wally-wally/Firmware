import path
import time

object = path.FileManagement("MyFile")

object.writeLine("Forward", "2")
object.writeLine("Right", "5")

time.sleep(1)

print(str(object.readLine(1)))

object.closeFile()
