import numpy as np
import cv2
img = cv2.imread("img/balloon.jpg")
img2 = img
e1 = cv2.getTickCount()
k1 = 0
try:
	img2.itemset((0,0,0),255)
	cv2.imshow("img",img)
	for i in range(0,img.shape[0]):
		for k in range(0,img.shape[1]):
			k1 = k
			img2.itemset((i,k,0),255)
			img2.itemset((i,k,1),255)
			img2.itemset((i,k,2),0)
			#if k%15 == 0:
				#cv2.imshow("img"+str(i)+str(k),img)
		cv2.imshow("img"+str(i)+str(k),img)
except KeyboardInterrupt:
	print i
	print k1
cv2.imshow("finalimg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
e2 = cv2.getTickCount()
time = (e2 - e1) / cv2.getTickFrequency()
print time

#382 : 510
#109 : 208
# BALLOON COORDS