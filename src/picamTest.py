import time as t
import picamera
import picamera.array
import cv2
import Constants
import numpy as np
import io
from Filter import Filter as f

camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
capture = picamera.array.PiRGBArray(camera, size=(640,480))
# image = np.empty((480, 640, 3), dtype=np.uint8)
filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)
# t.sleep(0.1)

imgs = [
"img/balloon.jpg",
"img/balloon2.jpg",
"img/balloon3.jpg",
"img/balloon1.jpeg",
"img/balloon2.jpeg",
"img/balloon3.jpeg",
"img/balloon4.jpeg",
"img/imgres.jpg",
"img/imgres-1.jpg",
"img/imgres-4.jpg",
"img/images-1.jpg",
"img/images-3.jpg",
"img/images-4.jpg",
"img/images-5.jpg",
"img/images.jpg",
"img/imgres-2.jpg",
"img/imgres-3.jpg",
"img/images-6.jpg"
]

numFrames = 0
time = 0

outputDir = "/home/pi/Documents/RocketProject/cv/src/outputs.txt"
doOutput = True
controlFrames = 5000 # Used to stop at a certain number of frames
waitDelay = 1
capType = 2

camera.start_preview()
t.sleep(5)
camera.stop_preview()

def outputs():
	global numFrames, time
	stream = io.BytesIO()
	for i in range(controlFrames):
        # This returns the stream for the camera to capture to
		
		yield stream
		stream.seek(0)

		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		open_cv_image = cv2.imdecode(data, 1)

		e1 = cv2.getTickCount()

		if filtering:
			filt.image = open_cv_image
			f, imagey, c, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
			output = filt.run(filt.image)

		numFrames += 1

		stream.seek(0)
		stream.truncate()

		e2 = cv2.getTickCount()
		time += (e2-e1)/cv2.getTickFrequency()

try:
	tot1 = cv2.getTickCount()
	if capType == 1:
		for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
			e1 = cv2.getTickCount() # Starttime

			# AREA OF INTEREST
			# for i in range(500):
			filt.image = frame.array
			filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
			coolImage = filt.run(filt.image)

			capture.truncate(0)
			capture.seek(0)

			cv2.imshow('frameN', coolImage)
			key = cv2.waitKey(waitDelay)
			
			# if key == ord('q'):
			# 	break

			e2 = cv2.getTickCount()
			time += (e2 - e1) / cv2.getTickFrequency()
			numFrames += 1

			if controlFrames != 0 and numFrames >= controlFrames:
				break
	elif capType == 2:
		camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
	else:
		raise TypeError("Incorrect capType! capType can only be between 1 and 2. capType=%i" % (capType))
except KeyboardInterrupt:
	pass


tot2 = cv2.getTickCount()
total = (tot2 - tot1) / cv2.getTickFrequency()
cv2.destroyAllWindows()
camera.close()

output = "\nTOTAL FILTER TIME:\t "+str(time)+"\n\nAVERAGE TIME PER FRAME:\t "+str(time/numFrames)+"\n\nAVERAGE FRAMES PER SECOND:\t "+str(1 / (time / numFrames))+"\n\nTOTAL TIME INCLUDING CAPTURE:\t "+str(total)+"\n\nAVERAGE TIME PER FRAME INCLUDING CAPTURE:\t "+str(total/numFrames)+"\n\nAVERAGE FRAMES PER SECOND INCLUDING CAPTURE:\t "+str(1 / (total/numFrames))+"\n\nSTOPPED AT FRAME:\t "+str(numFrames)+" OUT OF: "+str(controlFrames)+"\n\n"
print output
if doOutput:
	try:
		fil = open(outputDir, "r")
		fil.close()
	except:
		fil = open(outputDir, "w")
		fil.close()
	f = open(outputDir, "a")
	f.write(output)
	f.write("================================================================")
	f.write("\n\n")
	f.write("================================================================")
	f.close()
