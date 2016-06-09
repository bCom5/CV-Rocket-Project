import numpy as np
import cv2
import SaveableImage as si

img = si.SaveableImage("img/balloon.jpg")
orig = img.image
img.showRaw('original image')
img.image = cv2.blur(img.image, (5,5))
img.showRaw('blurred image1')
img.testKey()
img.image = orig
img.showRaw('original image')
img.image = cv2.GaussianBlur(img.image, (5,5), 0)
img.showRaw('blurred imageG')
img.testKey()
img.image = orig
img.showRaw('original image')
img.image = cv2.medianBlur(img.image, 5)
img.showRaw('blurred imageM')
img.testKey()
img.image = orig
img.showRaw('original image')
img.image = cv2.bilateralFilter(img.image, 9,75,75)
img.showRaw('blurred imageB')
img.testKey()