# Pi camera Consumtion: Filtering
# TAKE FORM THE QUEUE AND DO IMAGE PROCESSING ON THE FRAME!
import multiprocessing
import picamera
import picamera.array
import cv2
import Constants
import io
import numpy as np
from Filter import Filter as f
import PIL as pillow
from PIL import Image
import time as t

camera = picamera.PiCamera()
# camera.raw_format = 'bgr'
camera.resolution = (640,480)
camera.framerate = 80
capture = picamera.array.PiRGBArray(camera, size=(640,480))
filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)

outputDir = "/home/pi/Documents/RocketProject/cv/src/outputs.txt"
doOutput = True

numFrames = 0
controlFrames = 2000 # Used to stop at a certain number of frames
frameBuffer = 2 # Buffer for queue for frames, preferably low so that it is refreshed often The higher it is, the longer it takes to change course
time = 0
timeCapture = 0

queue = multiprocessing.Queue(frameBuffer)


def Consumer(queue):
	# OPTIMALLY, ADD A WAY TO PULL EVERY OTHER FRAME FROM QUEUE SO IM NOT STUCK 60 FRAMES BEHIND MISSING FRAMES LATER
	global time, numFrames
	print "STARTED TO CONSUME"
	while numFrames < controlFrames:
		e1 = cv2.getTickCount() # Starttime

		# AREA OF INTEREST
		# for i in range(500):
		filt.image = queue.get()
		filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
		coolImage = filt.run(filt.image)

		cv2.imshow('frame', coolImage)
		key = cv2.waitKey(0)
		
		# if key == ord('q'):
		# 	break

		e2 = cv2.getTickCount()
		time += (e2 - e1) / cv2.getTickFrequency()
		numFrames += 1
	print time, time / numFrames, 1 / (time/numFrames)
	print "STOPPED CONSUMING"
def Producer():
	global timeCapture, numFrames, time
	try:
		print "STARTED TO PRODUCE"
		tot1 = cv2.getTickCount()
		for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
			# e1 = cv2.getTickCount()

			# QUEUE FULL EXCEPTION
			try:
				queue.put(frame.array)
				# print "PUT AN IMAGE"
			except:
				print "TOO BIG!"
			# e2 = cv2.getTickCount()
			# timeCapture += (e2-e1) / cv2.getTickFrequency()

			capture.truncate(0)
			if controlFrames != 0 and numFrames >= controlFrames:
				print "STOPPED PRODUCING"
				break
			else:
				# print numFrames
				numFrames += 1
	except KeyboardInterrupt:
		# IT HAS ENDED
		pass
	tot2 = cv2.getTickCount()
	total = (tot2 - tot1) / cv2.getTickFrequency()
	cv2.destroyAllWindows()
	camera.close()

	time = 1.0 # CAUSE TIME IS BROKEN RIGHT NOW
	timeCapture = 1.0 # CAUSE TIME IS COMMENTED OUT ABOVE

def recordOutput():
	output = "\nTOTAL FILTER TIME:\t "+str(time)+"\n\nAVERAGE TIME PER FRAME:\t "+str(time/numFrames)+"\n\nAVERAGE FRAMES PER SECOND:\t "+str(1 / (time / numFrames))+"\n\nTOTAL TIME INCLUDING CAPTURE:\t "+str(total)+"\n\nAVERAGE TIME PER FRAME INCLUDING CAPTURE:\t "+str(total/numFrames)+"\n\nAVERAGE FRAMES PER SECOND INCLUDING CAPTURE:\t "+str(1 / (total/numFrames))+"\n\nTOTAL KNOWN CAPTURE TIME:\t "+str(timeCapture)+"\n\nAVERAGE CAPTURE TIME PER FRAME:\t "+str(timeCapture / numFrames)+"\n\nAVERAGE CAPTURE FPS:\t "+str(1/ (timeCapture / numFrames))+"\n\nSTOPPED AT FRAME:\t "+str(numFrames)+" OUT OF: "+str(controlFrames)+"\n\n"
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
	queue.close()
	queue.join_thread()
	p.join()

def outputs():
	global queue, numFrames
	stream = io.BytesIO()
	for i in range(controlFrames):
        # This returns the stream for the camera to capture to
		yield stream

		stream.seek(0)
		# pil_image = Image.open(stream)
		# open_cv_image = np.array(pil_image)

		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		open_cv_image = cv2.imdecode(data, 1)

		# cv2.imshow("tgest", open_cv_image)
		# cv2.waitKey(0)
		# open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

		try:
			numFrames += 1
			queue.put(open_cv_image)
		except:
			print "FULL QUEUE"
	    # Finally, reset the stream for the next capture
		stream.seek(0)
		stream.truncate()
	print "SHOULD BE DONE"

    # time.sleep(2)
def captureSequenceMethod():
	global timeCapture
	start = t.time()
	camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
	finish = t.time()
	timeCapture = finish - start
	print('Captured %s images at %.2ffps' % (controlFrames, (controlFrames / (finish - start))))

def consumerMethod():
	p.start()

tot1 = cv2.getTickCount()
p = multiprocessing.Process(target=Consumer, args=(queue,))

consumerMethod()

captureSequenceMethod()
# Producer()

tot2 = cv2.getTickCount()
total = (tot2-tot1) / cv2.getTickFrequency()

time = 1.0 # TIME IS BROKEN RIGHT NOW
# timeCapture = 1.0 # ALSO BROKEN

camera.close()
recordOutput()

