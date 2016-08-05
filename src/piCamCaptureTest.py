import picamera
import picamera.array
import multiprocessing
import numpy as np
import cv2
import time as t
import io

controlFrames = 500
numFrames = 0
frameBuffer = 500
timeCapture = 0

camera = picamera.PiCamera()
# camera.raw_format = 'bgr'
camera.resolution = (640,480)
camera.framerate = 80
capture = picamera.array.PiRGBArray(camera, size=(640,480))

queue = multiprocessing.Queue(frameBuffer)

def Consumer(queue):
	while numFrames < controlFrames:
		image = queue.get()
		numFrames += 1

def outputs():
	global queue, numFrames
	stream = io.BytesIO()
	for i in range(controlFrames):
        # This returns the stream for the camera to capture to
		yield stream

		stream.seek(0)
		# pil_image = Image.open(stream)
		# open_cv_image = np.array(pil_image)
		# print "STARTING DATA"

		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		open_cv_image = cv2.imdecode(data, 1)

		# cv2.imshow("tgest", open_cv_image)
		# cv2.waitKey(0)
		# open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

		try:
			numFrames += 1
			queue.put(open_cv_image)
			print numFrames, 
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


print "ONLY PRODUCING %f FRAMES!" % controlFrames
# print camera._get_settings()
p = multiprocessing.Process(target=Consumer, args=(queue,))
p.start()
captureSequenceMethod()