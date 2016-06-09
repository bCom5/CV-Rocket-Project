import numpy as np
import cv2
from SaveableImage import SaveableImage as si
from Filter import Filter as f

"""
Contour Finder + Filter Tester
By: Adam Noworolski (Sc2ad)

To use, place balloon images into the 'img' folder, then 


"""



pics = [
"img/balloon.jpg",
"img/balloon2.jpg",
"img/balloon3.jpg",
"img/balloon1.jpeg",
"img/balloon2.jpeg",
"img/balloon3.jpeg",
"img/balloon4.jpeg"
]

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
rgbConsts = {
	'rgbRedMin' : 105,
	'rgbRedMax' : 255,
	'rgbGreenMin' : 0,
	'rgbGreenMax' : 101,
	'rgbBlueMin' : 0,
	'rgbBlueMax' : 136
}
"""
allVals = {
	'cx': cx,
	'cy': cy,
	'A': A,
	'P': P,
	'k': k,
	'w': w,
	'h': h,
	'hull': hull,
	'ratio': aspect_ratio,
	'extent': extent,
	'solidity': solidity,
	'eD': eD,
	'angle': angle,
	'majorAxis': MA,
	'minorAxis': ma,
	'mask': mask,
	'pixelPoints': pixelPoints,
	'maxVal': max_val,
	'maxLocation': max_loc,
	'minVal': min_val,
	'minLocation': min_loc,
	'mean': mean,
	'leftMost': leftMost,
	'rightMost': rightMost,
	'topMost': topMost,
	'bottomMost', bottomMost
}
"""


filterLow = 115 # Binary Threshold Low Value
filterHigh = 255 # Binary Threshold High Value
filterType = cv2.ADAPTIVE_THRESH_GAUSSIAN_C # Type of Threshold Constant to use (1 or 0) listed below
# cv2.ADAPTIVE_THRESH_GAUSSIAN_C
# cv2.ADAPTIVE_THRESH_MEAN_C
# cv2.THRESH_BINARY
filterTypeNum = 2 # Number to use for filtering listed below
# 1 = Adaptive
# 2 = RGB
# 3 = Binary
size = 35 # Size of box to average for adaptive thresholds
c = 2 # Number to subtract result of adaptive threshold from

approx = cv2.CHAIN_APPROX_SIMPLE # Contour mappings: Map to shapes or dont map at all listed below
# cv2.CHAIN_APPROX_NONE


for item in pics:
	filt = f(cv2.imread(item),consts=consts, display=True)
	#grayimg = cv2.cvtColor(img.image, cv2.COLOR_BGR2GRAY)
	#ret, thresh = cv2.threshold(grayimg,127,255,0)
	#blur = cv2.GaussianBlur(grayimg,(5,5),0)
	img = si(item)
	im = cv2.imread(item)
	blur = filt.blur()
	img.showRaw("original")
	cv2.waitKey(0)
	img.image = blur
	img.showRaw("blurred")
	cv2.waitKey(0)
	if filterTypeNum == 1:
		filtered = cv2.adaptiveThreshold(img.image,filterHigh,filterType,cv2.THRESH_BINARY,size,c)
		img.image = filtered
		img.showRaw("threshed")
		cv2.waitKey(0)
		filtered, imagey, contours, h = filt.adaptiveGet(approx, filterHigh, size, c, filterType)
	elif filterTypeNum == 2:
		filtered, imagey, contours, h = filt.rgbGet(approx, rgbConsts)
		img.image = filtered
		img.showRaw("threshed")
		cv2.waitKey(0)
	else:
		ret3, filtered = cv2.threshold(blur, filterLow, filterHigh, filterType)#+cv2.THRESH_OTSU)
		img.image = filtered
		img.showRaw("threshed")
		cv2.waitKey(0)
		ret3, filtered, imagey, contours, h = filt.getContours(approx, filterLow, filterHigh, filterType)#+cv2.THRESH_OTSU)

	coolImage = filt.run(im)

	#img.image = coolImage
	# Draws contours on original image in COLOR
	img.image = coolImage
	img.showRaw("final")
	img.testKey()