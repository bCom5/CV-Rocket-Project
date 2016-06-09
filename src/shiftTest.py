import cv2
import numpy as np
import SaveableImage as si

img = si.SaveableImage("img/balloon.jpg")
img.title = 'img'
rows,cols = img.image.shape[:2]

M = np.float32([[1,0,100],[0,1,50]])
dst = cv2.warpAffine(img.image,M,(cols,rows))

img.image = dst
img.showRaw()
img.testKey()