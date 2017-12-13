import io
import cv2
import time
import numpy as np
import sys
import os
import picamera
from picamera.array import PiRGBArray
from base_camera import BaseCamera
if './../opencv' not in sys.path:
  sys.path.append('./../opencv')

from lane_detect import process_image
 
class Camera(BaseCamera):

    @staticmethod
    def auto_frames():
        # adding path
        
        with picamera.PiCamera() as camera:
            rawCapture = PiRGBArray(camera, size=(640, 480))
            # let camera warm up
            camera.resolution = (640, 480)
            camera.hflip = True
            camera.vflip = True
            time.sleep(2)
            for frame in camera.capture_continuous(rawCapture, 'bgr',
                                                 use_video_port=True):
                # return current frame
                #img = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY)
                img, cmd = process_image(frame.array)
                  
                status, buf = cv2.imencode('.jpeg', img)
                yield (np.array(buf).tostring(), cmd)
                
                
                rawCapture.truncate()
                rawCapture.seek(0)

    @staticmethod
    def rc_frames():
        with picamera.PiCamera() as camera:
            rawCapture = PiRGBArray(camera, size=(640, 480))
            # let camera warm up
            camera.resolution = (640, 480)
            camera.hflip = True
            camera.vflip = True
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
               stream.seek(0)
               yield stream.read()
               stream.seek(0)
               stream.truncate()

