import numpy as numpy
import cv2
quit = 0

Oimg = cv2.imread("img/balloon.jpg")
img = cv2.imread("img/balloon.jpg", 0)
cv2.namedWindow("Main Image", cv2.WINDOW_NORMAL)
cv2.imshow("Main Image", Oimg)
cv2.namedWindow("Other Image", cv2.WINDOW_NORMAL)
cv2.imshow("Other Image", img)
k = cv2.waitKey(0) & 0xFF
if k == 27 or k == ord("q"):
	print "Do you want to save your changes?"
	print "Pres 's' to save, 'q' to quit"
	cv2.waitKey(0) & 0xFF
	if k == ord("q"):
		cv2.destroyAllWindows()
		quit = 1
		print "Changes Discarded!"
	elif k == ord("s"):
		cv2.imwrite("img/grayBalloon.png", img)
		cv2.destroyAllWindows()
		quit = 1
		print "Changes Saved!"
elif k == ord("s"):
	cv2.imwrite("img/grayBalloon.png", img)
	cv2.destroyAllWindows()
	quit = 1
	print "Changes Saved!"
elif k == ord("a"):
	cv2.destroyWindow("Main Image")
	print "Main Image Destroyed!"
elif k == ord("d"):
	cv2.destroyWindow("Other Image")
	print "Secondary Image Destroyed!"
elif k == ord("e"):
	cv2.imshow("Main Image", Oimg)
	cv2.imshow("Other Image", img)
else:
	print "Incorrect key!"