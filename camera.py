from picamera import PiCamera
import os

IMG_FOLDER = './img/'

class Camera():

    def __init__(self):
        self.camera = PiCamera()

    def capture(self, imgName):
        self.camera.capture(IMG_FOLDER + imgName + '.jpeg')

    def rmImg(self, imgName):
        os.remove(IMG_FOLDER + imgName + '.jpeg')

