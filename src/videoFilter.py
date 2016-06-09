import numpy as np
import cv2
from SaveableImage import SaveableImage as si
from Filter import Filter as f

consts = {
	'minArea' : 55,
	'maxArea' : 20000,
	'minPerimeter' : 20,
	'maxPerimeter' : 3000,
	'minWidth' : 20,
	'maxWidth' : 600,
	'minHeight' : 25,
	'maxHeight' : 300,
	'minRatio' : 0.0,
	'maxRatio' : 1000.0,
	'minExtent' : 0.6,
	'maxExtent' : 0.9,
	'minSolidity' : 0.490,
	'maxSolidity' : 100.0,
	'minMean' : 0.0,
	'maxMean' : 255.0,
	'minVerticies' : 40,
	'maxVerticies' : 10200,
	'minAngle' : -360.0,
	'maxAngle' : 360.0,
	'minRatioWidthtoSize' : 0.05,
	'maxRatioWidthtoSize' : 0.4,
	'minRatioHeighttoSize' : 0.033,
	'maxRatioHeighttoSize' : 0.4,
	'tolerance' : 24 # Number of above conditions to be met for successful contour observation
}
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:
		e1 = cv2.getTickCount() # Starttime
		coolFrame = np.copy(frame) # Copies the frame
		filt = f(frame, consts=consts, display=False) # Filter Object
		ret3, filtered, imagey, contours, h = filt.getContours(cv2.CHAIN_APPROX_SIMPLE, 113, 255, cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
		coolImage = filt.run(coolFrame)
		cv2.imshow('frame',coolImage)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break # Quits when you press q
		e2 = cv2.getTickCount()
		time = (e2 - e1) / cv2.getTickFrequency()
		print time
	else:
		break
cap.release()
cv2.destroyAllWindows()