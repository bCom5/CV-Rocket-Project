import numpy as np
import cv2
import random
import SaveableImage as si

img = si.SaveableImage("img/balloon.jpg")
img.title = "IMG"
balloon = img.image[382:510, 109:208]
balloon2 = img.image[109:208, 382:510]
for c in range(0,random.randint(1,10)):
	i = random.randint(1,600-99)
	k = random.randint(1,800-128)
	img.image[i:i+99, k:k+128] = balloon2
img.showRaw()
img.testKey(outputName="img/img.png")