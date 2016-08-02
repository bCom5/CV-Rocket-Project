# Pi camera Consumtion: Filtering
# TAKE FORM THE QUEUE AND DO IMAGE PROCESSING ON THE FRAME!
import multiprocessing
import picamera
import picamera.array
import cv2
import Constants
from Filter import Filter as f

camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
capture = picamera.array.PiRGBArray(camera, size=(640,480))
filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)

outputDir = "/home/pi/Documents/RocketProject/cv/src/outputs.txt"
doOutput = True

numFrames = 0
controlFrames = 500 # Used to stop at a certain number of frames
frameBuffer = 60
time = 0
timeCapture = 0

queue = multiprocessing.Queue(frameBuffer)
p = multiprocessing.Process(target=Consumer, args=(queue,))


def Consumer(queue):
	global time, numFrames
	e1 = cv2.getTickCount() # Starttime
	# AREA OF INTEREST
	# for i in range(500):
	filt.image = queue.get()
	filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
	coolImage = filt.run(filt.image)
	# cv2.imshow('frameN', coolImage)
	# key = cv2.waitKey(1)
	
	# if key == ord('q'):
	# 	break
	e2 = cv2.getTickCount()
	time += (e2 - e1) / cv2.getTickFrequency()
	numFrames += 1
def Producer():
	global timeCapture
	try:
		tot1 = cv2.getTickCount()
		for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
			e1 = cv2.getTickCount()
			queue.put(frame.array)
			e2 = cv2.getTickCount()
			timeCapture += (e2-e1) / cv2.getTickFrequency()
			capture.truncate(0)
			if controlFrames != 0 and numFrames >= controlFrames:
				break
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

	queue.close()
    queue.join_thread()
    p.join()
p.start()
Producer()


