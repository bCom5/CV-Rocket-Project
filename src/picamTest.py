import time
import picamera
import picamera.array
import cv2
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

# Runs the filter until finished (press q)

# filt = f(cv2.imread("img/balloon.jpg"), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False) # Filter Object
# with picamera.PiCamera() as camera:
# 	camera.resolution = (640,480)
# 	camera.framerate = 30
# 	camera.shutter_speed = camera.exposure_speed
# 	camera.exposure_mode = 'off'
# 	g = camera.awb_gains
# 	camera.awb_mode = 'off'
# 	camera.awb_gains = g
# 	with picamera.array.PiRGBArray(camera) as stream:
# 		while True:
# 			#break
# 			piCamFilter(camera, stream)

camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
capture = picamera.array.PiRGBArray(camera, size=(640,480))
filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)
time.sleep(0.1)
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

# for img in imgs:
# 	for i in range(10):
# 		filt.image = cv2.imread(img)
# 		f, i, c, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
# 		coolImage = filt.run(filt.image)
# 		cv2.imshow('frame', coolImage)
# 		cv2.waitKey(0)

# 	filt.confidence.confidence = [0]


for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
	e1 = cv2.getTickCount() # Starttime
	# AREA OF INTEREST
	for i in range(500):
		filt.image = frame.array
		filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
		coolImage = filt.run(filt.image)
	capture.truncate(0)

	cv2.imshow('frameN', coolImage)
	#key = cv2.waitKey(1)
	e2 = cv2.getTickCount()
	time = (e2 - e1) / cv2.getTickFrequency()
	print time
	# if key == ord('q'):
	# 	break
cv2.destroyAllWindows()


