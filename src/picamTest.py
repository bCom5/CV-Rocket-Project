import time
import picamera
import picamera.array
import cv2
import picamera
import Constants
from Filter import Filter as f

def piCamFilter(camera, stream):
	e1 = cv2.getTickCount() # Starttime
	camera.capture(stream, format='bgr')
	frame = stream.array
	#coolFrame = np.copy(frame) # Copies the frame
	#filt = f(frame, consts=consts, display=False) # Filter Object
	filt.image = frame
	ret, filtered, imagey, contours, h = filt.getContours(cv2.CHAIN_APPROX_SIMPLE)
	coolImage = filt.run(frame)
	cv2.imshow('frame',coolImage)
	e2 = cv2.getTickCount()
	time = (e2 - e1) / cv2.getTickFrequency()
	print time
"""
# Saves first 10 seconds of footage to a file
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.resolution = (1280, 720)
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    with picamera.array.PiRGBArray(camera) as stream:
    	camera.resolution = (640, 480)
	    camera.start_recording('my_video.h264')
	    camera.wait_recording(10)
	    camera.stop_recording()
        #camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        #image = stream.array
"""

# Runs the filter until finished (press q)
filt = f(cv2.imread("img/balloon.jpg"), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False) # Filter Object
with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.framerate = 30
	camera.shutter_speed = camera.exposure_speed
	camera.exposure_mode = 'off'
	g = camera.awb_gains
	camera.awb_mode = 'off'
	camera.awb_gains = g
	with picamera.array.PiRGBArray(camera) as stream:
		while True:
			#break
			piCamFilter(camera, stream)

