# BASELINE
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
filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)

camera.start_preview()
t.sleep(5)
camera.stop_preview()

out = ""
time = 0
numFrames = 0

controlFrames = 500
testCount = 3
wantedTestTypes = [1,3]
filtering = True
outputDir = "Notes.txt"

def outputs():
	global numFrames, time
	stream = io.BytesIO()
	for i in range(controlFrames):
        # This returns the stream for the camera to capture to

		e1 = cv2.getTickCount()
		yield stream
		stream.seek(0)

		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		open_cv_image = cv2.imdecode(data, 1)

		if filtering:
			filt.image = open_cv_image
			f, i, c, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
			output = filt.run(filt.image)

		try:
			numFrames += 1
			# queue.put(open_cv_image) 
		except:
			print "FULL QUEUE"
		stream.seek(0)
		stream.truncate()

		e2 = cv2.getTickCount()
		time += (e2-e1)/cv2.getTickFrequency()

for i in range(testCount):
	breaking = False
	for cType in wantedTestTypes:
		time = 0
		numFrames = 0
		try:
			tot1 = cv2.getTickCount()
			if cType == 1:
				for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
					e1 = cv2.getTickCount() # Starttime

					if filtering:
						filt.image = frame.array
						filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
						output = filt.run(filt.image)

					capture.truncate(0)
					capture.seek(0)
					numFrames += 1
					if controlFrames != 0 and numFrames >= controlFrames:
						break
					e2 = cv2.getTickCount()
					time += (e2 - e1) / cv2.getTickFrequency()
			elif cType == 2:
				while numFrames < controlFrames:
					camera.capture(capture, format='bgr')
					e1 = cv2.getTickCount()
					
					if filtering:
						filt.image = capture.array
						f, imagey, c, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
						output = filt.run(filt.image)

					capture.truncate(0)
					capture.seek(0)
					e2 = cv2.getTickCount()
					time += (e2 - e1) / cv2.getTickFrequency()
					numFrames += 1
					if controlFrames != 0 and numFrames >= controlFrames:
						break
			elif cType == 3:
				camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
		except KeyboardInterrupt:
			breaking = True
		tot2 = cv2.getTickCount()
		totalTime = (tot2-tot1) / cv2.getTickFrequency()
		# print "Test %i with settings %i: Captured %i frames at total fps of %.2f, with internal fps of %.2f. Saw a contour in %i frames." % (i, cType, numFrames, numFrames/totalTime, numFrames/time, goodFrames)
		out += "Test %i with settings %i:\tCaptured %i frames at total fps of %.2f, with internal fps of %.2f. Saw a contour in %i frames.\n" % (i, cType, numFrames, numFrames/totalTime, numFrames/time, filt.contourCount)
	if breaking:
		print "BREAKING OUT"
		break
try:
	f = open(outputDir, "r")
except:
	f = open(outputDir, "w")
	f.write(str(outputDir)+": A place to store data from various Baseline tests.")
f.close()
print out
f = open(outputDir, "a")
f.write(out)
f.close()
