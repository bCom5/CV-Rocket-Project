import numpy as np
import cv2
from SaveableImage import SaveableImage as si
from Filter import Filter as f
import Constants

"""
Contour Finder + Filter Tester
By: Adam Noworolski (Sc2ad)

To use, place balloon images into the 'img' folder, then add them to the pics variable below
Variable 'consts' is all the constants that are used for contour filtering
Variable 'rgbConsts' is all the constants that are used for the RGB filter
"""



pics = [
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

consts = Constants.PHOTOS_CONTOUR_FILTER_CONSTANTS_1
# GOAL: TO HAVE MULTIPLE FILTER OBJECTS CORRESPONDING TO DIFFERENT DISTANCES: HAVE SOME IDEA
# OF HOW HIGH THE ROCKET IS AND USE THE FILTERS THAT MATCH THE HEIGHT (OTHERWISE, IT MIGHT BE
# VIRTUALLY IMPOSSIBLE TO HAVE A FILTER THAT 'FITS ALL')

rgbConsts = Constants.PHOTOS_RGB_FILTER_CONSTANTS_1

consts2 = Constants.PHOTOS_CONTOUR_FILTER_CONSTANTS_2

rgbConsts2 = Constants.PHOTOS_RGB_FILTER_CONSTANTS_2


filterLow = 115 # Binary Threshold Low Value
filterHigh = 255 # Binary Threshold High Value
filterType = cv2.ADAPTIVE_THRESH_GAUSSIAN_C # Type of Threshold Constant to use (1 or 0) listed below
# cv2.ADAPTIVE_THRESH_GAUSSIAN_C
# cv2.ADAPTIVE_THRESH_MEAN_C
# cv2.THRESH_BINARY
# cv2.THRESH_BINARY + cv2.THRESH_OTSU
filterTypeNum = 2 # Number to use for filtering listed below
# 1 = Adaptive
# 2 = RGB
# 3 = Binary
size = 35 # Size of box to average for adaptive thresholds
c = 2 # Number to subtract result of adaptive threshold from

approx = cv2.CHAIN_APPROX_SIMPLE # Contour mappings: Map to shapes or dont map at all listed below
# cv2.CHAIN_APPROX_NONE
# cv2.CHAIN_APPROX_SIMPLE


for item in pics:
	filt = f(cv2.imread(item),consts=consts, display=True) # Creates a filter object with the image, constants and displayability
	filt2 = f(cv2.imread(item), consts=consts2, display=True) # Another filter for second attempt
	#grayimg = cv2.cvtColor(img.image, cv2.COLOR_BGR2GRAY)
	#ret, thresh = cv2.threshold(grayimg,127,255,0)
	#blur = cv2.GaussianBlur(grayimg,(5,5),0)
	img = si(item) # Creates a savable image (an image that is saveable to the hard drive)
	im = cv2.imread(item) # Reads the same image again, 'im' is the original image
	# blur = filt.blur() # blurs the image using the filter object
	blur = im
	img.showRaw("original") # shows the image with title 'original'
	cv2.waitKey(0) # waits 0 milliseconds (forever) for a key to be pressed
	img.image = blur # sets the savable image to the blurred image
	img.showRaw("blurred") # shows the blurred iamge with title 'blurred'
	cv2.waitKey(0) 
	if filterTypeNum == 1: # If using adaptive thresholding
		filtered, imagey, contours, h = filt.adaptiveGet(approx, filterHigh, size, c, filterType) # gets the filtered binary image, the original image, the contours, and the hierarchy from the filter object
		img.image = filtered # Sets the saveable image to the filtered result
		img.showRaw("threshed") # Displays it with title 'threshed'
		cv2.waitKey(0)
	elif filterTypeNum == 2: # If using RGB thresholding
		filtered, imagey, contours, h = filt.rgbGet(approx, rgbConsts) # Uses RGB filtering through the filter object
		filtered2, imagey2, contours2, h2 = filt2.rgbGet(approx, rgbConsts2)
		img.image = filtered
		img.showRaw("threshed")
		cv2.waitKey(0)
		img.image = filtered2
		img.showRaw("threshed through filter 2")
		cv2.waitKey(0)
	else: # Otherwise, do normal thresholding (binary)
		ret, filtered, imagey, contours, h = filt.getContours(approx, filterLow, filterHigh, filterType) # Gets the ret as well from the normal thresholding from the filter object
		img.image = filtered
		img.showRaw("threshed")
		cv2.waitKey(0)

	#img.image = coolImage
	# Draws contours on original image in COLOR
	img.image = filt.run(im) # Filter.run(image) runs the filter which spits out the contours that pass the tolerance level of the constants above, see 'Filter.py' for more details
	img.showRaw("final")
	img.testKey() # Allows the final image to be saved, asks if you want to save it before quitting
	img.image = filt2.run(im)
	img.showRaw("final through filter 2")
	img.testKey()