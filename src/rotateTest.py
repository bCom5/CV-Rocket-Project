import cv2
import numpy as np
import SaveableImage as si

img = si.SaveableImage("img/balloon.jpg")
img.title = 'img'
rows,cols = img.shape()[:2]

M = cv2.getRotationMatrix2D((cols/2+60,rows/2+120),90,1)
dst = cv2.warpAffine(img.image,M,(cols,rows))

img.image = dst
img.showRaw()
img.testKey()