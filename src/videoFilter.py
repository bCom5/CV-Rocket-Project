import numpy as np
import cv2
from SaveableImage import SaveableImage as si
from Filter import Filter as f

consts = {
	'minArea' : 305,
	'maxArea' : 10000,
	'minPerimeter' : 200,
	'maxPerimeter' : 10000,
	'minWidth' : 100,
	'maxWidth' : 800,
	'minHeight' : 5,
	'maxHeight' : 10000,
	'tolerance' : 8
}
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:
		e1 = cv2.getTickCount()
		# write the flipped frame
		coolFrame = frame
		filt = f(frame, consts=consts, display=False)
		ret3, filtered, imagey, contours, h = filt.getContours(cv2.CHAIN_APPROX_SIMPLE, 113, 255, cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
		coolImage = filt.run(coolFrame)
		cv2.imshow('frame',coolImage)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		e2 = cv2.getTickCount()
		time = (e2 - e1) / cv2.getTickFrequency()
		print time
	else:
		break
cap.release()
cv2.destroyAllWindows()